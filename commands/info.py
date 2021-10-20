import discord
from discord.ext import commands

@commands.command(name = "info", aliases = ["information"], description = "Information about the bot")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def info(ctx):

    em = discord.Embed(title = "Bot Information", description = "This is a bot created by Morpheye#9690, as a discord game meant to simulate 45 strafing in Minecraft Parkour.", color = ctx.author.color)

    em.add_field(name = "Development Assistance", value = "bear_#7302 \ndude_guy_boy#3136")
    em.add_field(name = "Physics Help", value = "mine_pvpkill#8588 \nlavalaph#7013 \nBenjamaster7#9895 \nSrock#4106")
    em.add_field(name = "Beta Testing", value = "TBD")

    await ctx.send(embed = em)


def setup(bot):
    bot.add_command(info)
