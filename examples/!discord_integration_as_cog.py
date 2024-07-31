import discord
from discord.ext import commands, localization

class LocalizationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ = localization.Localization("cogs/discord_integration_as_cog.i18n.json", "en") # ! Because a cog is run from the main file, the path is relative to the main file!!!
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(self._("ping", ctx, latency=self.bot.latency * 1000))
        
def setup(bot):
    bot.add_cog(LocalizationCog(bot))
    print("Cog loaded!")