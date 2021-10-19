import discord
from discord.ext import commands

@commands.command(name = "help", description = "Command info")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "This is the full list of bot commands", color = ctx.author.color)

    em.add_field(name = "Information", value = "help \ninfo \nprofile")
    em.add_field(name = "Coin Making", value = "single45 \ndouble45 \ntriple45")

    await ctx.send(embed = em)


def setup(bot):
    bot.add_command(help)
