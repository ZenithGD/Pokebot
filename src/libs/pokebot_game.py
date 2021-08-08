import discord
from discord.enums import try_enum
import requests
import json

from discord.ext import commands
from libs.misc import MemberCast
from libs.exceptions import *

from enum import Enum, unique

class PokemonInstance:

    def __init__(self) -> None:
        pass

@unique
class PokeType(Enum):
    Normal      = 0,    "Normal"
    Fire        = 1,    "Fire"
    Water       = 2,    "Water"
    Grass       = 3,    "Grass"
    Electric    = 4,    "Electric"    
    Ice         = 5,    "Ice"
    Fighting    = 6,    "Fighting"    
    Poison      = 7,    "Poison"
    Ground      = 8,    "Ground"
    Flying      = 9,    "Flying"
    Psychic     = 10,   "Psychic"    
    Bug         = 11,   "Bug"
    Rock        = 12,   "Rock"
    Ghost       = 13,   "Ghost"
    Dragon      = 14,   "Dragon"    
    Dark        = 15,   "Dark"
    Steel       = 16,   "Steel"
    Fairy       = 17,   "Fairy"

class PokemonInfo:
    """General information about Pokémon.

    Attributes:
        type_chart (dict of PokeType:(list of float)): Represents the attack 
        multiplier for each attacking type for every defending type.

        Note: The i-th component in each list represents the attack multiplier
        against the type whose Poketype.value[0] = i. 
        
        For example:

            PokemonInfo.type_chart[PokeType.Fire][PokeType.Water.value] = 0.5,

        where PokeType.Water.value = 2, means that a fire Pokémon attacking a water
        Pokémon will deal half the damage to its opponent.
    """

    type_chart = {
        PokeType.Normal     : [1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1],
        PokeType.Fire       : [1,0.5,0.5,2,1,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1],
        PokeType.Water      : [1,2,0.5,0.5,1,1,1,1,2,1,1,1,2,1,0.5,1,1,1],
        PokeType.Grass      : [1,0.5,2,0.5,1,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1],
        PokeType.Electric   : [1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1],
        PokeType.Ice        : [1,0.5,0.5,2,1,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1],
        PokeType.Fighting   : [2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5],
        PokeType.Poison     : [1,1,1,2,1,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2],
        PokeType.Ground     : [1,2,1,0.5,2,1,1,2,1,0,1,0.5,2,1,1,1,2,1],
        PokeType.Flying     : [1,1,1,2,0.5,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1],
        PokeType.Psychic    : [1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1],
        PokeType.Bug        : [1,0.5,1,2,1,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5],
        PokeType.Rock       : [1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1],
        PokeType.Ghost      : [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,1,1],
        PokeType.Dragon     : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0],
        PokeType.Dark       : [1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,1,0.5],
        PokeType.Steel      : [1,0.5,0.5,1,0.5,2,1,1,1,1,1,1,2,1,1,1,0.5,2],
        PokeType.Fairy      : [1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1]
    }

    @staticmethod
    def get_multiplier(atk: PokeType, defn: PokeType) -> float: 

        return PokemonInfo.type_chart[atk][defn.value[0]]

    @staticmethod
    def get_pokemon_info(nm: str):

        # Get response from the API request
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nm.lower()}")
        
        if response:
            return response.json()
        else:
            raise InfoException(f"Can't find {nm} in database.")

    @staticmethod
    def get_all_pokemon():

        with open('res/names/names.json') as file:
            names = json.load(file)

        return [ pk['name'] for pk in names['results'] ]

class PokemonBattle:
    pass
    

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
            str: Prints the state of the current battle
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