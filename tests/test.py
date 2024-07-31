from discord.ext import localization

_ = localization.Localization("test_lang.json")
print(_.file)