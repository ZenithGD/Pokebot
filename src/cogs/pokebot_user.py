import discord
from discord.ext import commands
from discord_components.component import ButtonStyle
from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow

from libs.embeds import *
from libs.misc import *

class PokeBotUser(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -------------------------------------------------------------------------
    # Restricted commands: Can only be used by staff. Staff must have the
    # BotAdmin role in the server
    # -------------------------------------------------------------------------


    @commands.command(name="serverstats", description="Show bot usage and presence stats")
    async def serverstats(self, ctx):
        if commands.has_role(admin_role):
            await ctx.send(embed=uptime_embed(self.bot))
        else:
            await ctx.send("You don't have permission to run this command")

def setup(bot):
    bot.add_cog(PokeBotUser(bot))