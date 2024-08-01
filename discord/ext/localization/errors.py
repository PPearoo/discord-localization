class InvalidJSONFormat(ValueError):
    """Raised when there is incorrect formatting in the localization file."""
    def __init__(self, path: str):
        self.path = path
        self.message = "Invalid JSON format in localization file: '{}'".format(path)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class LocalizationFileNotFound(FileNotFoundError):
    """Raised when the localization file is not found."""
    def __init__(self, path: str):
        self.path = path
        self.message = "Localization file not found: '{}'".format(path)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class LocalizationNotFound(KeyError):
    """Raised when the localization is not found."""
    def __init__(self, text: str, locale: str):
        self.text = text
        self.locale = locale
        self.message = "Localization '{}' not found for locale '{}'".format(text, locale)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class InvalidLocale(KeyError):
    """Raised when the locale is not found."""
    def __init__(self, locale: str):
        self.locale = locale
        self.message = "Invalid locale '{}'".format(locale)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class WrongLocalizationFormat(TypeError):
    """Raised when the localization is not a list."""
    def __init__(self, locale: str, _type: type):
        self.locale = locale
        self.type = _type.__name__
        self.message = "Localization for locale '{}' must be of type list, received {}".format(locale, self.type)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message