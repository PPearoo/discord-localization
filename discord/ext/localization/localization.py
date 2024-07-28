import json
import logging
import os
from typing import Any, List, Optional, Sequence
from sys import argv

class Localization:
    """discord.py extension for command localization."""
    
    def __init__(self, filename: str, default_locale: Optional[str] = None) -> None:
        """
        Represents a localization object.
        
        -------
        ### Parameters:
            filename: :class:`str`
                The name of the file to load the translations from. This must be a JSON file.
            
            default_locale: Optional[:class:`str`]
                The default locale to use if the locale is not found in the translation.
        """
        script_path = os.path.abspath(argv[0])
        script_dir = os.path.dirname(script_path)
        
        self.filename: str = os.path.join(script_dir, filename)
        self.default_locale: str = default_locale
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.file: dict = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in translation file: {}".format(self.filename))

    def localize(self, text: str, language: str, **kwargs: Any) -> str | List[str]:
        """
        Gets the translation of a string like it's done in i18n.
        
        If `text` is not found in the translation file, or if there isn't a translation file, it returns `text` itself.
        
        -------
        ### Parameters:
            text: :class:`str`
                The key to find in the translation file.
            language: :class:`str`
                The 2-letter language code of the language you want to translate to.
            **kwargs: :class:`Any`
                The arguments to pass to the string formatter.
        
        -------
        ### Returns:
            `str`
                The translated string.
            List[:class:`str`]
                If the translation is a list, it returns the list of translated strings.
        """
        translations = self.file.get(language)
        if not translations:
            logging.error("No translations for language {}".format(language))
            return text
        trans_text = translations.get(text)
        if trans_text:
            if isinstance(trans_text, list):
                return [i.format(**kwargs) for i in translations[text]]
            return translations[text].format(**kwargs)
        else:
            logging.error("Translation for \"{}\" not found for language {}".format(text, language))
            return text
    
    _ = t = translate = localise = localize
    
    def one(self, text: str, number: int | float, language: str, **kwargs: Any) -> str:
        """
        Gets the singular and plural form of a string like it's done in i18n.
        
        For this, you need to have the key in the JSON be a list of two strings, the first being the singular form, the second being the plural form.
        
        -------
        ### Parameters:
            text: `str`
                The key to find in the translation file.
            lang: `str`
                The 2-letter language code of the language you want to translate to.
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
        trans = self.t(text, language, **kwargs)
        if not isinstance(trans, Sequence[str]):
            raise TypeError("Translation for \"{}\" is not a list".format(text))
        if not trans:
            return text
        if number == 1:
            return trans[0]
        else:
            return trans[-1]
        
    _o = o = one
    
    def __call__(self, text: str, language: str, **kwargs) -> str:
        """
        Gets the translation of a string like it's done in i18n.
        
        If `text` is not found in the translation file, or if there isn't a translation file, it returns `text` itself.
        
        -------
        ### Parameters:
            text: `str`
                The key to find in the translation file.
            lang: `str`
                The 2-letter language code of the language you want to translate to.
            **kwargs: `Any`
                The arguments to pass to the string formatter.
        
        -------
        ### Returns:
            `str`
                The translated string.
        """
        return self.localize(text, language, **kwargs)