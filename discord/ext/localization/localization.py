import json
import logging
import os
from typing import Any, List, Optional, Union
from sys import argv
from discord import Guild, Locale, Interaction
from discord.ext.commands import Context
from .errors import *

class Localization:
    """discord.py extension for command localization."""
    
    def __init__(self, relative_path: str, default_locale: Optional[str] = None, error: Optional[bool] = False) -> None:
        """
        Represents a localization object.
        
        -------
        ### Parameters:
            relative_path: :class:`str`
                The name of the file to load the localizations from. This must be a JSON file.
            default_locale: Optional[:class:`str`]
                The default locale to use if the locale is not found in the localization.
            error: Optional[:class:`bool`]
                Whether to raise an error if the localization is not found. If set to `False`, it will return the key itself. Defaults to `False`.
        """
        script_path = os.path.abspath(argv[0])
        script_dir = os.path.dirname(script_path)
        
        self.relative_path: str = os.path.join(script_dir, relative_path)
        """The relative path to the localization file."""
        self.default_locale: str = default_locale
        """A fallback locale that is used if a given locale is not found in the localization file."""
        self.error: bool = error
        """Whether the library should raise errors log them using `logging.error()`."""
        
        try:
            with open(self.relative_path, "r", encoding="utf-8") as f:
                self.file: dict = json.load(f)
                """The contents of the localization file."""
        except json.JSONDecodeError:
            raise InvalidJSONFormat(self.relative_path)
        except FileNotFoundError:
            raise LocalizationFileNotFound(self.relative_path)
    
    def format_strings(self, data: Any, **kwargs: Any) -> Any:
        """
        Formats the strings in a dictionary. This is used internally, to format strings in the :meth:`localize` method.
        
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
            return {key: self.format_strings(value, **kwargs) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.format_strings(item, **kwargs) for item in data]
        elif isinstance(data, str):
            return data.format(**kwargs)
        else:
            return data

    def localize(self, text: str, locale: Union[str, Locale, Guild, Interaction, Context], **kwargs: Any) -> Union[str, List[str], dict]:
        """
        Gets the localization of a string like it's done in i18n.
        
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


        
        localizations = self.file.get(locale) or self.file.get(self.default_locale)
        if not localizations:
            if self.error:
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
            if self.error:
                raise LocalizationNotFound(text, locale)
            else:
                logging.error(LocalizationNotFound(text, locale))
                return text
        
        return self.format_strings(value, **kwargs)
    
    _ = t = translate = localise = localize
    
    def one(self, text: str, number: Union[int, float], locale: Union[str, Locale, Guild, Interaction, Context], **kwargs: Any) -> str:
        """
        Gets the singular and plural form of a string like it's done in i18n.
        
        For this, you need to have the key in the JSON be a list of two strings, the first being the singular form, the second being the plural form.
        
        This method can raise any errors that the :meth:`localize` method can raise.
        
        Parameters
        ----------
        text: `str`
            The key to find in the localization file.
        number: `Union[int, float]`
            The number to determine whether to use the singular or plural form.
        locale: `str`
            The locale to find the localization with, or an object that has an attribute that returns :class:`discord.Locale`.
        
        Returns
        -------
        `str`: If `num` is 1, returns the first item of the list. Otherwise, it returns the last item of the list.
        
        Raises
        ------
        `WrongLocalizationFormat`: The localization key is not a list.
        """
        localized_text = self.localize(text, locale, **kwargs)

        if not isinstance(localized_text, list):
            if self.error:
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