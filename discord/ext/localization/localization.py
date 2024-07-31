import json
import logging
import os
from typing import Any, List, Optional, Sequence
from sys import argv
from discord import Guild, Locale

class Localization:
    """discord.py extension for command localization."""
    
    def __init__(self, relative_path: str, default_locale: Optional[str] = None, error: Optional[bool] = False) -> None:
        """
        Represents a localization object.
        
        -------
        ### Parameters:
            relative_path: :class:`str`
                The name of the file to load the translations from. This must be a JSON file.
            
            default_locale: Optional[:class:`str`]
                The default locale to use if the locale is not found in the translation.
            
            error: Optional[:class:`bool`]
                Whether to raise an error if the translation is not found. If set to `False`, it will return the key itself.
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
            raise ValueError("Invalid JSON format in translation file: {}".format(self.relative_path))

    def localize(self, text: str, locale: Optional[str | Locale], guild: Optional[Guild], **kwargs: Any) -> str | List[str]:
        """
        Gets the translation of a string like it's done in i18n.
        
        If `text` is not found in the translation file, or if there isn't a translation file, it returns `text` itself.
        
        -------
        ### Parameters:
            text: :class:`str`
                The key to find in the translation file.
            locale: Optional[:class:`str` | :class:`discord.Locale`]
                The locale of the language you want to translate to. Either this or the `guild` parameter must be provided.
            guild: Optional[:class:`discord.Guild`]
                The guild to get the locale from. If not provided, it will use the locale given in the `locale` parameter. Either this or the `locale` parameter must be provided.
            **kwargs: :class:`Any`
                The arguments to pass to the string formatter.
        
        -------
        ### Returns:
            `str`
                The translated string.
            List[:class:`str`]
                If the translation is a list, it returns the list of translated strings.
        """
        locale = str(locale) or str(guild.preferred_locale) # to accomodate for discord.Locale
        if not locale:
            if self.error:
                raise ValueError("No locale provided")
            else:
                logging.error("No locale provided")
                return text
        
        localizations = self.file.get(locale) or self.file.get(self.default_locale)
        if not localizations:
            if self.error:
                raise KeyError("No localizations for language {}".format(locale))
            else:
                logging.error("No localizations for language {}".format(locale))
                return text
        
        localized_text = localizations.get(text)
        if localized_text:
            if isinstance(localized_text, Sequence[str]):
                return [localized_item.format(**kwargs) for localized_item in localizations[text]]
            return localized_text.format(**kwargs)
        else:
            if self.error:
                raise KeyError("Localization \"{}\" not found for language {}".format(text, locale))
            else:
                logging.error("Localization \"{}\" not found for language {}".format(text, locale))
                return text
    
    _ = t = translate = localise = localize
    
    def one(self, text: str, number: int | float, locale: str, **kwargs: Any) -> str:
        """
        Gets the singular and plural form of a string like it's done in i18n.
        
        For this, you need to have the key in the JSON be a list of two strings, the first being the singular form, the second being the plural form.
        
        -------
        ### Parameters:
            text: `str`
                The key to find in the translation file.
            locale: `str`
                The locale of the language you want to translate to.
            num: `int` or `float`
                The number to decide which form to use.
            **kwargs: `Any`
                The arguments to pass to the string formatter.
                
        -------
        ### Returns:
            `str`
                If `num` is 1, returns the first item of the list.
                Otherwise, it returns the last item of the list.
                If the list only has 1 item, it returns that item.
        """
        
        localized_text = self.localize(text, locale, **kwargs)
        if not isinstance(localized_text, Sequence[str]):
            raise TypeError("Translation for \"{}\" is not a list".format(text))
        
        if not localized_text:
            if self.error:
                raise KeyError("Localization \"{}\" not found for language {}".format(text, locale))
            else:
                logging.error("Localization \"{}\" not found for language {}".format(text, locale))
                return text
        
        if number == 1:
            return localized_text[0]
        else:
            return localized_text[-1]
        
    _o = o = one
    
    __call__ = localize