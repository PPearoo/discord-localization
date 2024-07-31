from discord.ext import localization
import random

_ = localization.Localization("non-discord_usage.i18n.json", "en") # the first option is the relative path to the localization file. the second is the fallback/default language that is used if the actual language is not found.
dice = random.randint(1, 6)
language = input("What's your native language? / Was ist Deine Muttersprache? (en/de) >>> ")

print(_("dice_result", language, dice=dice))