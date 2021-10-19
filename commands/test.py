import discord
from discord.ext import commands

@commands.command(name = "test", description = "testing")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 1, commands.BucketType.user)
async def test(ctx):
    pass


def setup(bot):
    bot.add_command(test)
