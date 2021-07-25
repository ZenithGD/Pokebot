import libs.pokelogger

class PokeBotError(Exception):
    """A class for Pokébot exception handling and logging
    """
    def __init__(self, prefix: str, message: str):
        """Constructor for instancing a generic Pokébot error.

        Args:
            prefix (str): The tag to print before the message
            message (str): The exception message
        """
        self.prefix = prefix
        self.message = message

    def log(self):
        """Prints the message and the exception prefix in the log file
        """
        print(f"[{self.prefix}]: {self.message}")

class BattleException(PokeBotError):
    """A class for handling and logging exceptions during battle.
    """
    def __init__(self, message: str):
        """Constructor for instancing a battle exception.

        Args:
            message (str): The exception message
        """
        super.__init__("BATTLE_ERROR", message)