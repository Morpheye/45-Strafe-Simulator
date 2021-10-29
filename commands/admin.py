import discord, sqlite3, random
from discord.ext import commands
from db_functions import add_coins, add_xp, get_level, get_kriddytoo_shrine_boost, add_kriddytoo_shrine_boost
from datetime import datetime

@commands.command(name = "admin", description = "testing")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.is_owner()
@commands.cooldown(1, 1, commands.BucketType.user)
async def admin(ctx):
    if datetime.now().hour == 21 and datetime.now().minute == 47:
        await ctx.send("Balls")
    await ctx.send(datetime.now().hour)
    await ctx.send(datetime.now().minute)

    #db = sqlite3.connect('database.sqlite')
    #cursor = db.cursor()
    #cursor.execute(f"SELECT * FROM users")
    #result = cursor.fetchall()
    #for row in result:

    #    if row[6] == 0:
    #        cursor.execute(f"UPDATE users SET daily_streak = 0 WHERE id = {row[0]}")
    #    cursor.execute(f"UPDATE users SET has_claimed_daily = 0 WHERE id = {row[0]}")
    #db.commit()
    #cursor.close()
    #db.close()


def setup(bot):
    bot.add_command(admin)
