import discord
from discord.ext import commands


class PokeBotAdmin(commands.Cog):

    # Ensure the user has the BotAdmin role
    @commands.has_role("BotAdmin")
    @commands.command(name="show battles")
    async def show_battles(self, ctx):


