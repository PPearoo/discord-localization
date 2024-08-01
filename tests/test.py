from discord.ext import localization
from discord import Locale

_ = localization.Localization("test_lang.json", error=True)
print(_.file, _("world", Locale.taiwan_chinese))