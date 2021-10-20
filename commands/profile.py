import discord
from discord.ext import commands
from main import get_coins
from main import get_level
from main import get_xp


@commands.command(name = "profile", aliases = ["user", "coins", "balance", "bal", "money"], description = "Show your profile and coins")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def profile(ctx):


    em = discord.Embed(title = f"Profile of **{ctx.author}**", description = f"{ctx.author}'s 45 strafe profile", color = ctx.author.color)

    em.add_field(name = "Coins", value = f"{await get_coins(ctx.author.id)} :coin:")

    em.add_field(name = "Level", value = f"{await get_level(ctx.author.id)}\n(XP: {await get_xp(ctx.author.id)}/{((await get_level(ctx.author.id)) * 1000) + 1000})")

    await ctx.send(embed = em)


def setup(bot):
    bot.add_command(profile)
