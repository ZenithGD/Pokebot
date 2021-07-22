import discord
from discord.ext import commands, tasks

class BotHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        em = discord.Embed (
            title="Help Menu",
            description="Here's the main command groups you can use.\n" +
                        "For more info about them, type `!help <command>`."
        )

    async def send_group_help(self, group):
        pass

    async def send_cog_help(self, cog):
        pass

    async def send_command_help(self, cog):
        pass

    def command_not_found(self, string):
        pass

    def subcommand_not_found(self, string):
        pass