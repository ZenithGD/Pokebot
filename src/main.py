import discord
from discord.ext import commands, tasks
from discord_components.component import ButtonStyle
from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow
from libs.pokebot_help import *
from libs.embeds import *

import os

class PokeBot(commands.Bot):

    def __init__(self, command_prefix, help_command):
        super().__init__(command_prefix=command_prefix, help_command=help_command)
        self.uptime = -1

    # Start every looping task
    async def on_ready(self):
        print("Bot started successfully")
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


client = PokeBot(command_prefix="!", help_command=commands.DefaultHelpCommand())
DiscordComponents(client)

token = os.getenv('DISCORD_POKEBOT_TOKEN')

# Get cogs
initial_extensions = ['cogs.pokebot_battle', 'cogs.pokebot_info']

if __name__ == '__main__':

    # -----------------------------------------------------------
    # Save the resources locally
    # -----------------------------------------------------------

    # Load pwd
    path = os.getcwd()

    res_dirs = ["/res/sprites/berries","/res/sprites/items", "/res/sprites/pokemon"]
    for dir in res_dirs:
        
        os.makedirs(path + dir)

    # Load extensions
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(token)
