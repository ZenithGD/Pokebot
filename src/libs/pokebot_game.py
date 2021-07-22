import discord
from discord.ext import commands

class PokeBotError(Exception):
    def __init__(self, message):
        self.message = message

class BattleInfo:
    def __init__(self):
        self.player_pair = []

    def print_info(self):
        if len(self.player_pair) == 0:
            return "Empty"
        elif len(self.player_pair) == 1:
            return "{} waiting".format(self.player_pair[0])
        elif len(self.player_pair) == 2:
            return "{} vs. {}".format(self.player_pair[0], self.player_pair[1])

    # Check whether the battle room is full
    def is_full(self):
        return len(self.player_pair) == 2

    # Add player to battle
    def join_battle(self, player: str):
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

    def info_embed(self):
        em = discord.Embed(
            title="Ongoing battles",
            description="Here's a list of the current battles"
        )
        for k in self.battle_set:
            em.add_field(
                name="Battle room nº {}".format(k),
                value=self.battle_set[k].print_info()
            )
        return em

    # Creates a battle, allocates a slot in the battle set and returns the battle index
    def create_battle(self):
        # Naive solution for finding smallest positive integer not in set
        max_idx = max(self.battle_set.keys(), default=0)
        cur_idx = 1
        while cur_idx <= max_idx:
            if cur_idx not in self.battle_set.keys():
                break
            else:
                cur_idx = cur_idx + 1

        self.battle_set[cur_idx] = BattleInfo()
        return cur_idx

    def join_room(self, player: str, idx: int):
        if idx in self.battle_set:
            # Can throw PokeBotError if the battle is already full
            # or the player is already participating in this battle
            self.battle_set[idx].join_battle(player)
        else:
            raise PokeBotError("This battle doesn't exist")

    # Leave battle with index idx
    # idx: integer
    def leave_battle(self, idx):
        if idx in self.battle_set.keys():
            self.battle_set.pop(idx)

    def room_full(self, idx):
        return self.battle_set[idx].is_full()