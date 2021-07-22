import discord
from discord.ext import commands

admin_role: str = "PokeBotAdmin"

# Operations for getting information about members based on context
class MemberCast(commands.MemberConverter):

    # Get user display name based on user id
    async def get_display_name(self, ctx, id):
        member = await super().convert(ctx, id)
        return member.display_name