import discord, sqlite3, random
from discord.ext import commands
from db_functions import add_coins, add_xp, get_level, get_kriddytoo_shrine_boost, add_kriddytoo_shrine_boost
from datetime import datetime

@commands.command(name = "admin", description = "testing")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.is_owner()
@commands.cooldown(1, 1, commands.BucketType.user)
async def admin(ctx, args=None):
    if args is None:
        return await ctx.send("```Please input arguments.```")

    if args == "dailyreset":
        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        result = cursor.fetchall()
        for row in result:
            print(f"{row[0]} {row[6]}")
            if row[6] == 0:
                cursor.execute(f"UPDATE users SET daily_streak = 0 WHERE id = {row[0]}")
            cursor.execute(f"UPDATE users SET has_claimed_daily = 0 WHERE id = {row[0]}")
        print("Dailies have been reset!")
        await ctx.send("```Dailies have been reset!```")
        db.commit()
        cursor.close()
        db.close()

    if args == "test":
        canvas = '''
        :black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::red_square::black_large_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::green_square::green_square::green_square::green_square::black_large_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::green_square::green_square::green_square::green_square::green_square::green_square::black_large_square:
:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::black_large_square:
:black_large_square::blue_square::black_large_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square:
:green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square::green_square:'''
        em = discord.Embed(title = "Test Canvas", description = canvas, color = ctx.author.color)
        em.add_field(name = "Name", value = "Value")
        await ctx.send(embed = em)


def setup(bot):
    bot.add_command(admin)
