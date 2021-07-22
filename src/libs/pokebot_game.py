import discord
from discord.ext import commands
from libs.misc import MemberCast
from libs.exceptions import BattleException

class BattleInfo:
    """Class for storing the info of any battle.
    """
    def __init__(self):
        """[summary]
        """
        self.player_pair = []

    async def print_info(self, ctx: discord.ext.commands.Context) -> str:
        """[summary]

        Args:
            ctx (discord.ext.commands.Context): The Discord context for extracting the 

        Returns:
            str: [description]
        """
        if len(self.player_pair) == 0:
            return "Empty"
        elif len(self.player_pair) == 1:
            return "{} waiting".format(
                await MemberCast().get_display_name(ctx, self.player_pair[0])
            )
        elif len(self.player_pair) == 2:
            return "{} vs. {}".format(
                await MemberCast().get_display_name(ctx, self.player_pair[0]),
                await MemberCast().get_display_name(ctx, self.player_pair[1])
            )

    # Check whether the battle room is empty
    def is_empty(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.player_pair == []

    # Check whether the battle room is full
    def is_full(self) -> bool:
        return len(self.player_pair) == 2

    # Add player to battle
    def join_battle(self, player: int):
        """[summary]

        Args:
            player (int): [description]

        Raises:
            BattleException: [description]
        """
        if not self.is_full():
            self.player_pair.append(player)
        else:
            raise BattleException("This battle is already full")

    # Remove player from room
    def leave_battle(self, player: str):
        if player in self.player_pair:
            self.player_pair.remove(player)

# Manager class for creating, leaving and joining battles
class BattleManager:

    def __init__(self):
        # Create the battle set
        # Add a placeholder
        self.battle_set = dict()

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

    def join_room(self, player: int, idx: int):
        if idx in self.battle_set:
            self.battle_set[idx].join_battle(player)
        else:
            raise BattleException("This battle doesn't exist")

    
    def leave_battle(self, player: int, idx: int):
        if idx in self.battle_set.keys():
            self.battle_set[idx].leave_battle(player)
            if self.battle_set[idx].is_empty():
                self.battle_set.pop(idx)

    def room_full(self, idx):
        return self.battle_set[idx].is_full()