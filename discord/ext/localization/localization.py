import json
import logging
import os
from typing import Any, List, Optional, Union, Self
from sys import argv
from discord import Guild, Locale, Interaction
from discord.ext.commands import Context
from .errors import *
import yaml

class Localization:
    """Represents an object that can be later used as a reference to localize strings.
    
    .. container:: operations
        
        .. describe:: x == y
            
            Checks if two instances are the same.
                
        .. describe:: x != y
                
            Checks if two instances are not the same.
            
        .. describe:: dict(x)
        
            Returns the dictionary containing the localizations.
    
    Attributes
    ----------
    localizations: Union[:class:`str`, :class:`dict`]
        :class:`str` - The relative path to the localization file, either a JSON or YAML file.
        :class:`dict` - The dictionary containing the localizations.
    default_locale: Optional[:class:`str`]
        The default locale to use if the locale is not found in the localization.
    error: Optional[:class:`bool`]
        Whether to raise an error if the localization is not found. If set to `False`, it will return the key itself. Defaults to `False`.
    """
    
    def __init__(
        self,
        localizations: Union[str, dict],
        default_locale: Optional[str] = None,
        error: Optional[bool] = False
    ) -> None:
        script_path = os.path.abspath(argv[0])
        script_dir = os.path.dirname(script_path)
        
        if isinstance(localizations, str):
            self._localizations: str = os.path.join(script_dir, localizations)
        elif isinstance(localizations, dict):
            self._localizations: dict = localizations
            
        self._default_locale: str = default_locale
        self._error: bool = error
        
        
        try:
            if isinstance(localizations, str):
                if localizations.endswith(".json"):
                    with open(self._localizations, "r", encoding="utf-8") as f:
                        self._file: dict = json.load(f)
                elif localizations.endswith(".yaml") or localizations.endswith(".yml"):
                    with open(self._localizations, "r", encoding="utf-8") as f:
                        self._file: dict = yaml.safe_load(f)
                        
            elif isinstance(localizations, dict):
                self._file: dict = localizations
                
        except json.JSONDecodeError:
            raise InvalidJSONFormat(self._localizations)
        except FileNotFoundError:
            raise LocalizationFileNotFound(self._localizations)
        
    @property
    def localizations(self) -> Union[str, dict]:
        """A path to the localization file or a dictionary containing the localizations.
        
        Setting this to a value after the object has been created will reload the localizations."""
        return self._localizations
    
    @localizations.setter
    def localizations(self, value: Union[str, dict]) -> None:
        script_path = os.path.abspath(argv[0])
        script_dir = os.path.dirname(script_path)
        
        if isinstance(value, str):
            self._localizations: str = os.path.join(script_dir, value)
        elif isinstance(value, dict):
            self._localizations: dict = value
        
        try:
            if isinstance(value, str):
                if value.endswith(".json"):
                    with open(self._localizations, "r", encoding="utf-8") as f:
                        self._file: dict = json.load(f)
                elif value.endswith(".yaml") or value.endswith(".yml"):
                    with open(self._localizations, "r", encoding="utf-8") as f:
                        self._file: dict = yaml.safe_load(f)
                        
            elif isinstance(value, dict):
                self._file: dict = value
                
        except json.JSONDecodeError:
            raise InvalidJSONFormat(self._localizations)
        except FileNotFoundError:
            raise LocalizationFileNotFound(self._localizations)
    
    @property
    def default_locale(self) -> Optional[str]:
        """A fallback locale that is used if a given locale is not found in the localization file."""
        return self._default_locale

    @default_locale.setter
    def default_locale(self, value: Optional[str]) -> None:
        self._default_locale: str = value
    
    @property
    def error(self) -> Optional[bool]:
        """Whether the library should raise errors (`True`) or log them using `logging.error()` (`False`)."""
        return self._error
    
    @error.setter
    def error(self, value: Optional[bool]) -> None:
        self._error: bool = value
    
    @property
    def file(self) -> dict:
        """The dictionary containing the localizations."""
        return self._file
    
    @file.setter
    def file(self, value: dict) -> None:
        self._file: dict = value
    
    def __eq__(self, other: Self) -> bool:
        return (self.file == other.file)
    
    def __ne__(self, other: Self) -> bool:
        return (self.file != other.file)
    
    def __repr__(self) -> str:
        if isinstance(self.localizations, str):
            return f"<Localization localizations={self.localizations!r} default_locale={self.default_locale!r} error={self.error!r} file={self._file}>"
        elif isinstance(self.localizations, dict):
            return f"<Localization localizations={self.localizations} default_locale={self.default_locale!r} error={self.error!r}>"
    
    def __dict__(self) -> dict:
        return self._file
    
    @staticmethod
    def format_strings(data: Any, **kwargs: Any) -> Any:
        """Formats the strings in a dictionary. This is used internally, to format strings in the :meth:`localize` method.
        
        It's not recommended to use this method in your code.
        
        Parameters
        ----------
        data: Any
            The data to format.
        **kwargs: Any
            The arguments to pass to the string formatter.
        
        Returns
        -------
        Any: The formatted data.
        """
        if isinstance(data, dict):
            return {key: Localization.format_strings(value, **kwargs) for key, value in data.items()}
        elif isinstance(data, list):
            return [Localization.format_strings(item, **kwargs) for item in data]
        elif isinstance(data, str):
            return data.format(**kwargs)
        else:
            return data

    def localize(self, text: str, locale: Union[str, Locale, Guild, Interaction, Context], **kwargs: Any) -> Union[str, List[str], dict]:
        """Gets the localization of a string like it's done in i18n.
        
        Parameters
        ----------
        text: :class:`str`
            The key to find in the localization file.
        locale: Union[:class:`str`, :class:`discord.Locale`, :class:`discord.Guild`, :class:`discord.Interaction`, :class:`discord.ext.commands.Context`]
            The locale to find the localization with, or an object that has an attribute that returns :class:`discord.Locale`.
        **kwargs: Any
            The arguments to pass to the string formatter.
        
        Returns
        -------
        Union[:class:`str`, List[:class:`str`], :class:`dict`]: The localized data.
        
        Raises
        ------
        `TypeError`: The locale parameter received an incorrect type.
        `InvalidLocale`: The locale parameter is not found in the localization file.
        `LocalizationNotFound`: The localization key is not found in the localization file.
        """
        if isinstance(locale, Guild):
            locale = str(locale.preferred_locale)
        elif isinstance(locale, (Interaction, Context)):
            locale = str(locale.guild.preferred_locale)
        elif isinstance(locale, (Locale, str)):
            locale = str(locale)
        else:
            raise TypeError("Locale must be of type str, discord.Locale, discord.Guild, discord.Interaction, or discord.ext.commands.Context, received {}".format(type(locale)))
        
        localizations = self._file.get(locale) or self._file.get(self._default_locale)
        if not localizations:
            if self._error:
                raise InvalidLocale(locale)
            else:
                logging.error(InvalidLocale(locale))
                return text
        
        if "." in text:
            keys = text.split(".")
            value = localizations
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                    if value is None:
                        break
                else:
                    value = None
                    break
        else:
            value = localizations.get(text)
        
        if value is None:
            if self._error:
                raise LocalizationNotFound(text, locale)
            else:
                logging.error(LocalizationNotFound(text, locale))
                return text
        
        return self.format_strings(value, **kwargs)
    
    _ = t = translate = localise = localize
    
    def one(self, text: str, number: Union[int, float], locale: Union[str, Locale, Guild, Interaction, Context], **kwargs: Any) -> str:
        """Gets the singular and plural form of a string like it's done in i18n.
        
        For this, you need to have the key in the JSON be a list of two strings, the first being the singular form, the second being the plural form.
        
        This method can raise any errors that the :meth:`localize` method can raise.
        
        Parameters
        ----------
        text: :class:`str`
            The key to find in the localization file.
        number: Union[:class:`int`, :class:`float`]
            The number to determine whether to use the singular or plural form.
        locale: :class:`str`
            The locale to find the localization with, or an object that has an attribute that returns :class:`discord.Locale`.
        
        Returns
        -------
        :class:`str`: If `num` is 1, returns the first item of the list. Otherwise, it returns the last item of the list.
        
        Raises
        ------
        `WrongLocalizationFormat`: The localization key is not a list.
        """
        localized_text = self.localize(text, locale, **kwargs)

        if not isinstance(localized_text, list):
            if self._error:
                raise WrongLocalizationFormat(locale, type(localized_text))
            else:
                logging.error(WrongLocalizationFormat(locale, type(localized_text)))
                return text
        
        if number == 1:
            return localized_text[0]
        else:
            return localized_text[-1]
        
    _o = o = one
    
    __call__ = localize
