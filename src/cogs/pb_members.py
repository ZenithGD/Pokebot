import discord
from discord.ext import commands, tasks

class PokeBotError(Exception):
    def __init__(self, message):
        self.message = message

class BattleInfo:
    def __init__(self):
        self.player_pair = []

    # Check whether the battle room is full
    def is_full(self):
        return len(self.player_pair) == 2

    # Add player to battle
    def join_battle(self, player):
        if not self.is_full():
            self.player_pair.append(player)
        else:
            raise PokeBotError("This battle is already full")

# Manager class for creating, leaving and joining battles
class BattleManager:
    def __init__(self):
        # Create the battle set
        # Add a placeholder
        self.battle_set = dict()
        self.battle_set[0] = BattleInfo()

    # Creates a battle, allocates a slot in the battle set and returns the battle index
    def create_battle(self):
        # Naive solution for finding smallest positive integer not in set
        max_idx = max(self.battle_set.keys())
        cur_idx = 1
        while cur_idx <= max_idx:
            if cur_idx not in self.battle_set.keys():
                break
            else:
                cur_idx = cur_idx + 1

        self.battle_set[cur_idx] = BattleInfo()
        return cur_idx

    def join_room(self, player, idx):
        if idx in self.battle_set:
            self.battle_set[idx].join_battle(player)
        else:
            raise PokeBotError("This battle doesn't exist")

    # Leave battle with index idx
    # idx: integer
    def leave_battle(self, idx):
        if idx in self.battle_set.keys():
            self.battle_set.pop(idx)

# Cog for member commands
class PokeBotMembers(commands.Cog):
    def __init__(self, bot, bm):
        self.bot = bot

        # Associate usernames with battle indexes
        self.battle_map = dict()

        # Manage ongoing battles
        self.battle_mgr = bm

    @commands.command()
    async def battle(self, ctx, arg, room=None):

        if arg == "start":
            if ctx.message.author.id in self.battle_map.keys():
                await ctx.send("You are already in a battle!")
            else:
                battle_index = self.battle_mgr.create_battle()
                self.battle_map[ctx.message.author.id] = battle_index
                print("{} created a battle".format(ctx.message.author.id))
                em = discord.Embed(
                    title="You created a new battle successfully!"
                )
                em.add_field(
                    name="Room number",
                    value=str(battle_index),
                    inline=True
                )

                await ctx.send(embed=em)

        elif arg == "leave":
            if ctx.message.author.id not in self.battle_map:
                await ctx.send("You are not participating in any battle!")
            else:
                self.battle_mgr.leave_battle(self.battle_map[ctx.message.author.id])
                self.battle_map.pop(ctx.message.author.id)
                await ctx.send("You left the battle.")

        elif arg == "join":
            try:
                self.battle_mgr.join_room(ctx.message.author.id, int(room))
            except Exception as xc:
                print(str(xc))


def setup(bot):
    bm = BattleManager()

    bot.add_cog(PokeBotMembers(bot, bm))
