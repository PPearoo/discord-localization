from discord.ext.localization import Localization

_ = Localization("test_lang.json")
apples = int(input("How many apples do you have? >>> "))
locale = input("What's your locale? >>> ")
if apples == 1:
    print(_.localize("apples.one", locale, apples=apples))
elif apples == 3:
    print(_.localize("apples.three", locale, apples=apples))
else:
    print(_.localize("apples.many", locale, apples=apples))