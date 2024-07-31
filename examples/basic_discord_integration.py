import discord
from discord.ext import commands, localization

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # hey guys, breaking the 4th wall here. please stop using Intents.default() just to set the message_content intent to True right after. Intents.all() does it for you.
_ = localization.Localization("basic_discord_integration.i18n.json", "en")

@bot.event
async def on_ready():
   print("Bot is ready!")

@bot.command()
async def ping(ctx):
   await ctx.reply(_("ping", ctx, latency=bot.latency * 1000))
   
bot.run('token')