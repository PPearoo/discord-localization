from discord.ext import localization
import logging

_ = localization.Localization("test_lang.json")._
print(_("hello", "hu"))