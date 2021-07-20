import discord
from discord.ext import commands

class PokeBotMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_map = []

    @commands.command()
    async def battle(self, ctx):



