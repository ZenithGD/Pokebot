import discord
from discord.ext import commands
from discord_components.component import ButtonStyle
from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow

# Currying
from functools import partial

# TODO: optimize imports
from libs.embeds import *
from libs.misc import *
from libs.pokebot_game import *
from libs.pokelogger import *

class Pokeprint:
    @staticmethod
    def typeinfo_str(types: list, mult: str) -> str:
        s =  "\n".join([ "* " + s for s in [s.name for s in types]])
        if mult is None:
            return s
        else:
            return s + f"\n**Multiplier**: {mult}"

class PokeBotUser(commands.Cog):

    def __init__(self, bot, logger):

        # The discord bot object
        self.bot = bot

        # Hold reference to main logger
        self.logger = logger

    # -------------------------------------------------------------------------
    # Public commands: Can be used by anyone
    # -------------------------------------------------------------------------

    @commands.group(name="info", description="General info about Pokémon/Pokébot")
    async def info(self, ctx: commands.Context):
        """Command group for general information about Pokémon/Pokébot.

        If the subcommand doesn't exist, it will send a message.

        Note: Every info subcommand should be in this group.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("This sub command doesn't exist.")
            
    
    @info.command(name="typechart", description="Show the type chart and multipliers.")
    async def typechart(self, ctx: commands.Context):
        em = discord.Embed(title="Type chart")
        em.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Pokemon_Type_Chart.svg/1026px-Pokemon_Type_Chart.svg.png")
        await ctx.send(embed=em)

    @info.command(name="type", description="Get general information about this Pokémon type")
    async def type(self, ctx: commands.Context, target_type: str):

        if target_type.capitalize() not in [ s.value[1] for s in PokeType ]:
            em = discord.Embed(title="Type doesn't exist", description="Available types: \n" + Pokeprint.typeinfo_str(PokeType, None))
            await ctx.send(embed=em)
        else:
            em = discord.Embed(
                title=f"Information about {target_type.capitalize()} type",
                color=discord.Color.blurple()
            )

            # Get lists of effective, normal, less effective and ineffective types 
            # defending from PokeType[target_type]:

            x0, x05, x1, x2 = [], [], [], []

            for t in PokeType:
                multiplier = PokemonInfo.get_multiplier(PokeType[target_type.capitalize()], t)
                if multiplier == 0:
                    x0.append(t)
                elif multiplier == 0.5:
                    x05.append(t)
                elif multiplier == 1:
                    x1.append(t)
                else:
                    x2.append(t)


            # Print embed with fields for each degree of effectiveness
            em.add_field(
                name="✨ Effective against",
                value=Pokeprint.typeinfo_str(x2, "x2"),
                inline=True
            )
            em.add_field(
                name="✅ Normal against",
                value=Pokeprint.typeinfo_str(x1, "x1"),
                inline=True
            )
            em.add_field(
                name="❌ Less effective against",
                value=Pokeprint.typeinfo_str(x05, "x0.5"),
                inline=True
            )
            em.add_field(
                name="☠ Ineffective against",
                value=Pokeprint.typeinfo_str(x0, "x0"),
                inline=True
            )

            await ctx.send(embed=em)

    @info.command()
    async def pokedex(self, ctx: commands.Context, nm: str):

        """print(json_info['types'])
            return json_info['id'], \
                   json_info['name'], \
                   json_info['height'], \
                   json_info['weight'], \
                   [ t['type']['name'] for t in json_info['types'] ], \
                   json_info['sprites']['front_default']
        """
        try:
            poke_info = PokemonInfo.get_pokemon_info(nm)

            # Pokémon's types
            types = [ t['type']['name'] for t in poke_info['types'] ]

            embed = discord.Embed(
                title=f"Pokemon Information"
            )
            embed.set_thumbnail(url=poke_info['sprites']['front_default'])
            embed.add_field(name="Pokédex ID", value=f"#{poke_info['id']}", inline=True)
            embed.add_field(name="Name", value=poke_info['name'], inline=True )
            embed.add_field(name="Height", value=f"{float(poke_info['height']) / 10.0} m", inline=True )
            embed.add_field(name="Weight", value=f"{float(poke_info['weight']) / 10.0} kg", inline=True )
            embed.add_field(name="Types", 
                            value=", ".join([ s.capitalize() for s in types ]), 
                            inline=True )
            await ctx.send(embed=embed)
        except PokeBotError as xc:

            embed = discord.Embed(
                title="Oops!",
                description=f"We can't find {nm} in the Pokédex. Maybe you meant:"
            )
            i = 1
            for e in sorted(PokemonInfo.get_all_pokemon(), key=partial(levenshtein_distance, nm))[:5]:
                embed.add_field(
                    name=f"{i}º",
                    value=e,
                    inline=True
                )
                i = i+1
            
            await ctx.send(embed=embed)
            xc.log()


    # -------------------------------------------------------------------------
    # Restricted commands: Can only be used by staff. Staff must have the
    # BotAdmin role in the server
    # -------------------------------------------------------------------------

    @commands.command(name="serverstats", description="Show bot usage and presence stats")
    async def serverstats(self, ctx: commands.Context):
        if commands.has_role(admin_role):
            await ctx.send(embed=uptime_embed(self.bot))
        else:
            await ctx.send("You don't have permission to run this command!")

def setup(bot):
    bot.add_cog(PokeBotUser(bot, bot.logger))