import discord
from discord.ext import commands, tasks
import os

class PokeBot(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)
        self.uptime = 0

    def uptime_embed(self):
        # Create an embed with a title
        em = discord.Embed(
            title="Pokébot",
            description="A little Pokémon battle simulator",
            color=int("90d080", 16)
        )
        em.add_field(name="Servers running",
                     value="{} servers".format(len(self.guilds)),
                     inline=True
                     )
        em.add_field(
            name="Uptime",
            value="{} days, {} hours, {} minutes".format(self.uptime / 1440,
                                                         (self.uptime % 1440) / 60,
                                                         self.uptime % 60),
            inline=True
        )
        return em

    # Start every looping task
    async def on_ready(self):
        self.idleLoop.start()
        self.updateUptime.start()

    # Show bot stats every hour
    @tasks.loop(seconds=3600)
    async def idleLoop(self):
        activity = discord.Game(name="Pokébot", type=discord.ActivityType.playing)
        await self.change_presence(status=discord.Status.idle, activity=activity)
        em = self.uptime_embed()
        channel = self.get_channel(866767487222415380)
        await channel.send(embed=em)

    # Increase uptime every minute
    @tasks.loop(seconds=60)
    async def updateUptime(self):
        self.uptime = self.uptime + 1


client = PokeBot(command_prefix="!")
token = os.getenv('DISCORD_POKEBOT_TOKEN')

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.pb_members']

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(token)