import discord, sqlite3, random
import math
from main import bot
from discord.ext import commands
from db_functions import add_coins, add_xp, get_level, get_kriddytoo_shrine_boost, add_kriddytoo_shrine_boost
from datetime import datetime

@commands.command(name = "admin", description = "testing")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.is_owner()
@commands.cooldown(1, 1, commands.BucketType.user)
async def admin(ctx, subcommand=None, args1=None, args2=None, args3=None):

    if subcommand is None:
        return await ctx.send("```Please input arguments.```")

    if subcommand == "test":

        if float(args1) < 0.0:
            facing = 180 * (math.pi / 180)
        else:
            facing = 0 * (math.pi / 180)

        trajectory = []

        #tick 1
        jump_speed_x = abs(float(args1)) * math.cos(facing)
        jump_speed_y = abs(float(args2))
        airtime = int(args3)

        total_speed_x = jump_speed_x
        total_speed_y = jump_speed_y

        print(f"B/T Speed: {jump_speed_x}, {jump_speed_y}, Total Speed: {total_speed_x}, {total_speed_y}")
        trajectory.append((round(total_speed_x),round(total_speed_y)))

        jump_speed_x = (jump_speed_x * 0.91 * 0.6) + (0.02 * 1.3 * math.cos(facing))
        jump_speed_y = (jump_speed_y - 0.08) * 0.98

        total_speed_x = total_speed_x + jump_speed_x
        total_speed_y = total_speed_y + jump_speed_y

        print(f"B/T Speed: {jump_speed_x}, {jump_speed_y}, Total Speed: {total_speed_x}, {total_speed_y}")
        trajectory.append((round(total_speed_x),round(total_speed_y)))

        for i in range(airtime-3):
            jump_speed_x = (jump_speed_x * 0.91) + (0.02 * 1.3 * math.cos(facing))
            total_speed_x = total_speed_x + jump_speed_x

            jump_speed_y = (jump_speed_y - 0.08) * 0.98
            total_speed_y = total_speed_y + jump_speed_y

            print(f"B/T Speed: {jump_speed_x}, {jump_speed_y}, Total Speed: {total_speed_x}, {total_speed_y}")
            trajectory.append((round(total_speed_x),round(total_speed_y)))

        jump_speed_y = (jump_speed_y - 0.08) * 0.98
        total_speed_y = total_speed_y + jump_speed_y

        print(f"B/T Speed: {jump_speed_x}, {jump_speed_y}, Total Speed: {total_speed_x}, {total_speed_y}")
        trajectory.append((round(total_speed_x),round(total_speed_y)))
        
        await ctx.send(f"Final speeds: {jump_speed_x}, {jump_speed_y}")
        await ctx.send(f"Distance covered: {total_speed_x}, {total_speed_y}")
        await ctx.send('\n'.join(map(str, trajectory)))



    if subcommand == "dailyreset":
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

    if subcommand == "reloadcommand":
        try:
            bot.reload_extension(f'commands.{args1}')
            await ctx.send(f"```Reloaded extension {args1}```")
            print(f"```Extension command.{args1} was reloaded```")
        except:
            await ctx.send("```That command does not exist```")

    if subcommand == "addcoins":
        try:
            await add_coins(int(args1), int(args2))
            await ctx.send(f"```Given {args2} coins to id {args1}```")
        except:
            await ctx.send(f"```Something went wrong trying to do this.```")
            


def setup(bot):
    bot.add_command(admin)
