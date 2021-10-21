import discord
from discord.ext import commands
from db_functions import add_coins, add_xp, get_level, get_kriddytoo_shrine_boost, add_kriddytoo_shrine_boost

@commands.command(name = "test", description = "testing")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 1, commands.BucketType.user)
async def test(ctx):
    pass


def setup(bot):
    bot.add_command(test)
