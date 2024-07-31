
from discord.ext.localization import Localization
import locale

_ = Localization("plurals.i18n.json")
apples = int(input("How many apples do you have? >>> "))
language = locale.getlocale()[0][:2] # this will return the default OS language, such as En, Hu, De, Fr, Es etc.

print(_.one("apples", apples, language.lower(), apples=apples))