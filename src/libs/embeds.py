import discord

def uptime_embed(bot):
    # Create an embed with a title
    em = discord.Embed(
        title="Pokébot",
        description="A little Pokémon battle simulator",
        color=int("90d080", 16)
    )
    em.add_field(name="Servers running",
                 value="{} servers".format(len(bot.guilds)),
                 inline=True
                 )
    em.add_field(
        name="Uptime",
        value="{} days, {} hours, {} minutes".format(bot.uptime // 1440,
                                                     (bot.uptime % 1440) // 60,
                                                     bot.uptime % 60),
        inline=True
    )
    return em
