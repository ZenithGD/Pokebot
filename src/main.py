import discord
from discord.ext import commands, tasks
from discord_components.component import ButtonStyle
from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow
from libs.pokebot_help import *
from libs.embeds import *

import os

from libs.pokelogger import * 

class PokeBot(commands.Bot):

    def __init__(self, command_prefix, help_command, logger: PokeLogger):
        super().__init__(command_prefix=command_prefix, help_command=help_command)
        self.logger = logger
        self.uptime = -1

    # Start every looping task
    async def on_ready(self):
        self.logger.log("Bot started successfully")
        self.update_uptime.start()
        self.idle_loop.start()

    # Show bot stats every 5 minutes
    @tasks.loop(seconds=300)
    async def idle_loop(self):
        activity = discord.Game(name="Pokébot", type=discord.ActivityType.playing)
        em = uptime_embed(self)
        channel = self.get_channel(866767487222415380)
        await channel.send(embed=em)

    # Increase uptime every minute
    @tasks.loop(seconds=60)
    async def update_uptime(self):
        self.uptime = self.uptime + 1

# TODO: Improve exception safety and handling
if __name__ == '__main__':

    # -----------------------------------------------------------
    # Create local folder structure and load data
    # -----------------------------------------------------------

    # Load pwd
    path = os.getcwd()

    # Initialize logging system
    log_dir = path + "/log"
    os.makedirs(log_dir, exist_ok=True)

    logger = PokeLogger(log_dir + "/info.log",
                        log_dir + "/warn.log",
                        log_dir + "/err.log")

    logger.log("Initialized logging", LogLevel.INFO)

    # Folder path declarations
    res_dirs = [path + "/res/sprites/berries",
                path + "/res/sprites/items", 
                path + "/res/sprites/pokemon"]

    # Create needed folders
    for dir in res_dirs:
        os.makedirs(dir, exist_ok=True)
        logger.log(f"Created folder at {dir}", LogLevel.INFO)

    client = PokeBot(command_prefix="!", 
                     help_command=commands.DefaultHelpCommand(), 
                     logger=logger
                    )

    DiscordComponents(client)

    token = os.getenv('DISCORD_POKEBOT_TOKEN')

    # Get cogs
    initial_extensions = ['cogs.pokebot_battle', 'cogs.pokebot_info', 'cogs.pokebot_catch']

    # Load extensions
    for extension in initial_extensions:
        logger.log(f"Loading {extension}...", LogLevel.INFO)
        try:
            client.load_extension(extension)
        except discord.DiscordException as xc:
            logger.log(f"Error while loading {extension}. Aborting...", LogLevel.ERR)
            raise xc

        logger.log("Done.", LogLevel.INFO)

client.run(token)
