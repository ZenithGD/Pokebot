from logging import disable
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button
from discord_components.component import ButtonStyle
from libs.exceptions import PokeBotError

from libs.pokebot_game import *
from libs.embeds import *
from libs.misc import *

# Cog for member commands
class PokeBotBattle(commands.Cog):

    """Cog for managing Pokébot battles

    Attributes:
        bot (commands.Bot): The bot associated with the cog.
        battle_map (dict): Association between Discord user IDs and battle rooms.
        battle_mgr (BattleManager): Manages the battle system
    """
    def __init__(self, bot: commands.Bot, bm: BattleManager):
        """Constructor for initializing the battle cog.

        Args:
            bot (commands.Bot): The bot to which the cog will be added.
            bm (BattleManager): The battle manager
        """
        self.bot = bot

        # Associate usernames with battle indexes
        self.battle_map = dict()

        # Manage ongoing battles
        self.battle_mgr = bm

    # -------------------------------------------------------------------------
    # Public commands: Can be used by anyone
    # -------------------------------------------------------------------------

    @commands.group(name="battle", description="Command group for PokéBot battles")
    async def battle(self, ctx: commands.Context):
        """Command group for battles.

        If the subcommand doesn't exist, it will send a message.

        Note: Every battle subcommand should be in this group.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("This sub command doesn't exist.")

    # TODO: Hold a list of pending battle room messages and delete those after 30 minutes
    @battle.command(name="start", description="Start a battle and generate room number")
    async def start(self, ctx: commands.Context):
        """Battle subcommand for starting a battle room.

        Creates a new room, indexed by a positive integer and sends an
        embed with the room number and a button in order to join the battle.

        Notes: 
            The message will be visible to any user in the channel until the room
        is full.

            An info message will be sent when the user who clicks the join button
            is already participating in another battle.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """

        # Check if user is already in a battle
        if ctx.message.author.id in self.battle_map.keys():
            await ctx.send("You are already in a battle!")
        else:

            # Generate index and allocate room for the battle
            battle_index = self.battle_mgr.create_battle()
            print("{} created a battle".format(ctx.message.author.display_name))

            # Room number embed
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

                    try:
                        # Join the room 
                        self.battle_mgr.join_room(interaction.user.id, int(battle_index))
                        
                        # Associate the user who interacted with the button with the room
                        self.battle_map[interaction.user.id] = battle_index

                        print("{} joined room nº {}.".format(interaction.user.display_name, battle_index))
                        await interaction.respond(content="You joined room nº {}.".format(battle_index))
                    except PokeBotError as xc:
                        xc.log()

                else:
                    await interaction.respond(content="You are already in a battle!")

            # Delete the embed when the room is full
            await msg.delete()

    # Command for leaving the current room.
    @battle.command(name="leave", description="Leave the battle room you are currently in")
    async def leave(self, ctx: commands.Context):
        """Battle subcommand for leaving a battle room.

        If the user is already participating in a battle, the user will leave the room.
        Otherwise, an info message will be sent.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """
        # Check whether the user is participating in a battle
        if ctx.message.author.id not in self.battle_map:
            await ctx.send("You are not participating in any battle!")
        else:
            self.battle_mgr.leave_battle(ctx.message.author.id, self.battle_map[ctx.message.author.id])
            self.battle_map.pop(ctx.message.author.id)
            print("{} left the battle.".format(ctx.message.author.id))
            await ctx.send("You left the battle.")

    # Join any given room if it exists
    @battle.command(name="join", description="Join a battle room")
    async def join(self, ctx: commands.Context, room: int):
        """Battle subcommand for joining any given room.

        If the user is not participating in any other battle, it will join
        room nº <room>. Otherwise, an info message will be se

        Args:
            ctx (commands.Context: The context in which the command was invoked.
            room (int): The index of the battle room
        """

        # Check whether the user is already participating in a battle
        if ctx.message.author.id in self.battle_map.keys():
            await ctx.send("You are already in a battle!")
        else:
            try:
                # Associate the user who interacted with the button with the room
                self.battle_map[ctx.message.author.id] = room

                # Join the room
                self.battle_mgr.join_room(ctx.message.author.id, int(room))
                await ctx.send("You joined room nº {}".format(room))
                print("{} joined room nº {}.".format(ctx.message.author.id, room))
            except PokeBotError as xc:
                xc.log()

    @commands.command(name="show_battles")
    async def show_battles(self, ctx):
        """Show a list of the ongoing battles

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """
        embed = discord.Embed(
            title="Battle rooms",
            description="Here's a list of the current battles"
        )
        for k in self.battle_mgr.battle_set:
            embed.add_field(
                name="Room nº {}".format(k),
                value=await self.battle_mgr.battle_set[k].print_info(ctx),
                inline=True
            )
        await ctx.send(embed=embed)

    # -------------------------------------------------------------------------
    # Restricted commands: Can only be used by staff. Staff must have the
    # BotAdmin role in the server
    # -------------------------------------------------------------------------

def setup(bot):
    bm = BattleManager()
    bot.add_cog(PokeBotBattle(bot, bm))
