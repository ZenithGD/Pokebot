import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button
from discord_components.component import ButtonStyle

from src.libs.pokebot_game import *
from src.libs.embeds import *
from src.libs.misc import *

# Cog for member commands
class PokeBotBattle(commands.Cog):
    def __init__(self, bot, bm: BattleManager):
        self.bot = bot

        # Associate usernames with battle indexes
        self.battle_map = dict()

        # Manage ongoing battles
        self.battle_mgr = bm

    # -------------------------------------------------------------------------
    # Public commands: Can be used by anyone
    # -------------------------------------------------------------------------

    @commands.group(name="battle", description="Command group for PokéBot battles")
    async def battle(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("This sub command doesn't exist.")

    @battle.command(name="start", description="Start a battle and generate room number")
    async def start(self, ctx: discord.ext.commands.Context):
        if ctx.message.author.id in self.battle_map.keys():
            await ctx.send("You are already in a battle!")
        else:
            battle_index = self.battle_mgr.create_battle()
            print("{} created a battle".format(ctx.message.author.id))
            em = discord.Embed(
                title="You created a new battle successfully!"
            )
            em.add_field(
                name="Room number",
                value=str(battle_index),
                inline=True
            )

            await ctx.send(
                embed=em,
                components=[Button(style=ButtonStyle.blue, label="Join battle", id="em")]
            )

            # Manage button response
            await self.bot.wait_for("button_click")
            for _ in range(2):
                await self.join(ctx, battle_index)

    @battle.command(name="leave", description="s")
    async def leave(self, ctx):
        if ctx.message.author.id not in self.battle_map:
            await ctx.send("You are not participating in any battle!")
        else:
            self.battle_mgr.leave_battle(self.battle_map[ctx.message.author.id])
            self.battle_map.pop(ctx.message.author.id)
            print("{} left the battle.".format(ctx.message.author.id))
            await ctx.send("You left the battle.")

    @battle.command()
    async def join(self, ctx, room):
        if ctx.message.author.id in self.battle_map.keys():
            await ctx.send("You are already in a battle!")
        else:
            self.battle_map[ctx.message.author.id] = room
            try:
                self.battle_mgr.join_room(ctx.message.author.display_name, int(room))
                print("{} joined room nº {}.".format(ctx.message.author.id, room))
            except Exception as xc:
                print(str(xc))

    @commands.command(name="show_battles")
    async def show_battles(self, ctx):
        await ctx.send(embed=self.battle_mgr.info_embed())

    # -------------------------------------------------------------------------
    # Restricted commands: Can only be used by staff. Staff must have the
    # BotAdmin role in the server
    # -------------------------------------------------------------------------

def setup(bot):
    bm = BattleManager()
    bot.add_cog(PokeBotBattle(bot, bm))
