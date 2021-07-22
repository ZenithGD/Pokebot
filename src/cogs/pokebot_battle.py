from logging import disable
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button
from discord_components.component import ButtonStyle

from libs.pokebot_game import *
from libs.embeds import *
from libs.misc import *

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

    # Battle command group. 
    @commands.group(name="battle", description="Command group for PokéBot battles")
    async def battle(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("This sub command doesn't exist.")

    # Battle start command.
    @battle.command(name="start", description="Start a battle and generate room number")
    async def start(self, ctx: discord.ext.commands.Context):

        # Check if user is already in a battle
        if ctx.message.author.id in self.battle_map.keys():
            await ctx.send("You are already in a battle!")
        else:

            # Generate index and allocate room for the battle
            battle_index = self.battle_mgr.create_battle()
            print("{} created a battle".format(ctx.message.author.id))

            # Basic embed
            em = discord.Embed(
                title="You created a new battle successfully!"
            )
            em.add_field(
                name="Room number",
                value=str(battle_index),
                inline=True
            )

            # Interaction button for easy joining
            btn = Button(style=ButtonStyle.blue, custom_id='0', label="Join battle")
            msg = await ctx.send(
                embed=em,
                components=[btn],
            )

            # Allow 2 people to join the room
            while not self.battle_mgr.room_full(battle_index):

                # Get interaction object when the user clicks
                interaction = await self.bot.wait_for("button_click")

                # Check if user is already in a battle
                if interaction.user.id not in self.battle_map.keys():

                    # Associate the user who interacted with the button with the room
                    self.battle_map[interaction.user.id] = battle_index

                    # Join the room 
                    try:
                        self.battle_mgr.join_room(interaction.user.display_name, int(battle_index))
                        print("{} joined room nº {}.".format(interaction.user.display_name, battle_index))
                        await interaction.respond(content="You joined room nº {}.".format(battle_index))
                    except Exception as xc:
                        print(str(xc))

                else:
                    await interaction.respond(content="You are already in a battle!")

            # Delete the embed when the room is full
            await msg.delete()

    # Command for leaving the current room.
    @battle.command(name="leave", description="Leave a battle room")
    async def leave(self, ctx):

        # Check whether the user is participating in a battle
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
