import discord
from discord.ext import commands
from libs.pokelogger import *
from libs.pokebot_game import PokemonInfo, PokeType, PokemonInstance


class PokeBotCatch(commands.Cog):

    def __init__(self, bot: commands.Bot, logger: PokeLogger):
        self.bot = bot
        self.logger = logger

def setup(bot):
    bot.add_cog(PokeBotCatch(bot, bot.logger))