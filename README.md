[Github](https://github.com/PearooXD/discord-localization) | [PyPI](https://pypi.org/project/discord-localization/)

--------
## Setting up
 Start by downloading the package via pip.
 ```
 python3 -m pip install discord-localization
 ```

 After that, you can just import it into your file as a discord.py extension.

--------
## Examples
 ```py
 from discord.ext import localization
 import random
 
 _ = localization.Localization("main.i18n.json", "en") # the first option is the relative path to the localization file. the second is the fallback/default language that is used if the actual language is not found.
 dice = random.randint(1, 6)
 language = input("What's your native language? / Was ist Deine Muttersprache? (en/de) >>> ")
 
 print(_("dice_result", language, dice=dice))
 ```
 ```json
 {
    "en": {
        "dice_result": "Your dice rolled {dice}!"
    },
    "de": {
        "dice_result": "Dein Würfel hat eine {dice} gewürfelt!"
    }
 }
 ```

## Integrating it into your Discord bot
 ```py
 import discord
 from discord.ext import commands, localization

 bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # hey guys, breaking the 4th wall here. please stop using Intents.default() just to set the message_content intent to True right after. Intents.all() does it for you.
 _ = localization.Localization("main_localization.json", "en")
 
 @bot.event
 async def on_ready():
    print("Bot is ready!")

 @bot.command()
 async def ping(ctx):
    await ctx.reply(_("ping", ctx, latency=bot.latency * 1000))
 ```
 ```json
 {
    "en": {
        "ping": "Pong! {latency}ms"
    },
    "en-US": {
        "ping": "Pong! {latency}ms, but American! (because Discord makes a difference between en-US and en-UK locales - you can circumvent this by setting the default_locale)"
    },
    "en-UK": {
        "ping": "Ping is {latency}ms, innit, bruv? (i'm sorry)"
    },
    "fr": {
        "ping": "Bonjour! Ping is {latency}ms!"
    }
 }
 ```
 Explanation:
 - By setting the default locale to "en", we won't have any issues with unfinished localizations. This way, we are also not required to define localizations for both "en-US" and "en-UK" (since Discord's API differentiates them, however, usually, bots don't.)
 - We are passing a `latency` argument to the localization function (which is also available with `Localization._`! But calling the object is fine too.), which will be later used whenever we use `{latency}` in a localization.
 - We are defining an `en` locale in the JSON file, even though both Discord's API and discord.py doesn't have such a locale. This is to make it more obvious that everything in that locale should be in English - you could also name it `default_locale`, you just have to make sure to edit it in the `Localization` object.
 - We pass `ctx` to the localization function, which will automatically try getting `ctx.guild.preferred_locale`. This works with `Interaction` (by using `Interaction.guild.preferred_locale` internally), `Guild` (by using `guild.preferred_locale` internally), or just passing the `Locale` itself, for example, `discord.Locale.american_english` (which will convert to the `en-US` locale).

-------
## Working with plurals
 ```py
 from discord.ext.localization import Localization
 import locale
 
 _ = Localization("main_plurals.json") # this will look for main_plurals.json as the language JSON file
 apples = int(input("How many apples do you have? >>> "))
 language = locale.getlocale()[0][:2] # this will return the default OS language, such as en, hu, de, fr, es etc.
 
 print(_.one("apples", apples, language, apples=apples))
 ```
 ```json
 {
     "en": {
         "apples": ["You only have one apple! What a loser...", "You have {apples} apples!"]
     },
     "hu": {
         "apples": ["{apples} almád van!"]
     }
 }
 ```

 This example does a great job at presenting how the `.one()` function works. Here's the explanation for the code:

 The code will look for the default OS language, and will tell you how many apples you have with plurals in mind. I always get angry when I see "you have 1 apples"-ish text on a website, and it's an easy fix, but for some reason, many developers don't pay attention to it.

 Hungarian doesn't make a difference between plurals, so the list for "hu"/"apples" only has 1 item. This won't be a problem though - the library isn't hardcoded to only look for the first and second elements in the returned list, it will look for the **first** and the **last**. Which means that if a list only has 1 item, it will only return that item.