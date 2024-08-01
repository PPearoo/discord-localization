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
        self.default_locale: str = default_locale
        self.error: bool = error
        
        try:
            with open(self.relative_path, "r", encoding="utf-8") as f:
                self.file: dict = json.load(f)
        except json.JSONDecodeError:
            raise InvalidJSONFormat(self.relative_path)
        except FileNotFoundError:
            raise LocalizationFileNotFound(self.relative_path)

    def localize(self, text: str, locale: Union[str, Locale, Guild, Interaction, Context], **kwargs: Any) -> Union[str, List[str]]:
        """
        Gets the localization of a string like it's done in i18n.
        
        -------
        ### Parameters:
            text: :class:`str`
                The key to find in the localization file.
            locale: Union[:class:`str` | :class:`discord.Locale` | :class:`discord.Guild` | :class:`discord.Interaction` | :class:`discord.commands.ext.Context`]
                The locale to find the localization with, or an object that has an attribute that returns :class:`discord.Locale`.
            **kwargs: :class:`Any`
                The arguments to pass to the string formatter.
        
        -------
        ### Returns:
            :class:`str`: The localized string.
            List[:class:`str`]: If the localization is a list, it returns the list of localized strings.
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
        
        localized_text = localizations.get(text)
        if localized_text:
            if isinstance(localized_text, list):
                return [localized_item.format(**kwargs) for localized_item in localizations[text]]
            return localized_text.format(**kwargs)
        else:
            if self.error:
                raise LocalizationNotFound(text, locale)
            else:
                logging.error(LocalizationNotFound(text, locale))
                return text
    
    _ = t = translate = localise = localize
    
    def one(self, text: str, number: Union[int, float], locale: str, **kwargs: Any) -> str:
        """
        Gets the singular and plural form of a string like it's done in i18n.
        
        For this, you need to have the key in the JSON be a list of two strings, the first being the singular form, the second being the plural form.
        
        -------
        ### Parameters:
            text: :class:`str`
                The key to find in the localization file.
            number: Union[:class:`int`, :class:`float`]
                The number to determine whether to use the singular or plural form.
            locale: Union[:class:`str` | :class:`discord.Locale` | :class:`discord.Guild` | :class:`discord.Interaction` | :class:`discord.commands.ext.Context`]
                The locale to find the localization with, or an object that has an attribute that returns :class:`discord.Locale`.
            **kwargs: `Any`
                The arguments to pass to the string formatter.
                
        -------
        ### Returns:
            :class:`str`: If `num` is 1, returns the first item of the list. Otherwise, it returns the last item of the list. If the list only has 1 item, it returns that item.
        """
        if isinstance(locale, Guild):
            locale = str(locale.preferred_locale)
        elif isinstance(locale, (Interaction, Context)):
            locale = str(locale.guild.preferred_locale)
        elif isinstance(locale, (Locale, str)):
            locale = str(locale)
        else:
            raise TypeError("Locale must be of type str, discord.Locale, discord.Guild, discord.Interaction, or discord.ext.commands.Context, received {}".format(type(locale)))
        
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