import discord
from discord.ext import commands, tasks

class BattleInfo:
    def __init__(self):
        pass

class BattleManager:
    def __init__(self):
        # Create the battle set
        # Add a placeholder
        self.battle_set = {0: BattleInfo()}

    # Naive solution for finding smallest positive integer not in set
    # Creates a battle, allocates a slot in the battle set and returns the battle index
    def create_battle(self):
        max_idx = max(self.battle_set.keys())
        cur_idx = 1
        while cur_idx <= max_idx:
            if cur_idx not in self.battle_set.keys():
                break
            else:
                cur_idx = cur_idx + 1

        self.battle_set[cur_idx] = BattleInfo()
        print("Battle with index {} created.".format(cur_idx))
        return cur_idx

    # L
    def leave_battle(self, idx):
        if idx in self.battle_set.keys():
            self.battle_set.pop(idx)
            print("Someone left the battle with index {}".format(idx))

class PokeBotMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_map = dict()
        self.battle_mgr = BattleManager()

    @commands.command()
    async def battle(self, ctx, arg):

        if arg == "start":
            if ctx.author in self.battle_map.keys():
                await ctx.send("You are already in a battle!")
            else:
                self.battle_map[ctx.author] = self.battle_mgr.create_battle()
                await ctx.send("You joined the battle succesfully!")

        elif arg == "leave":
            if ctx.author not in self.battle_map:
                await ctx.send("You are not participating in any battle!")
            else:
                self.battle_mgr.leave_battle(self.battle_map[ctx.author])
                self.battle_map.pop(ctx.author)
                await ctx.send("You left the battle.")



def setup(bot):
    bot.add_cog(PokeBotMembers(bot))
