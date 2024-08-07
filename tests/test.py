from discord.ext import localization
import pprint

_ = localization.Localization("test_lang.json", error=True)
pprint.pprint(_("test", "hu", a="EXAMPLE"))