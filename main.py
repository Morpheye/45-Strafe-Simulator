import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import *
import sqlite3
import os
from dotenv import load_dotenv
import random
from datetime import datetime

load_dotenv()
#environment variables

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = "?", intents = discord.Intents.all(), activity = discord.Game(name = "MCPK"))
bot.remove_command('help')

#stop console from logging "command not found"
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, CommandOnCooldown):
        await ctx.send(f"You must wait **{error.retry_after:.2f}** seconds before doing this again, **{ctx.author}**", delete_after = 5)
        return
    elif isinstance(error, NotOwner):
        await ctx.send(f"**{ctx.author} GET THE FUCK OUT OF HERE. RIGHT NOW.**")
        return
    raise error
 
@bot.event
async def on_ready():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    print(f"Logged in as {bot.user}!")

text = [
    "BWMM",
    "Pandora's Box",
    "GCXV",
    "Arcade3",
    "Triple 45 Strafe Journey",
    "Facade",
    "The Consistency Trial",
    "Onejump Lobby",
    "Linkcraft",
    "Huhucraft",
    "Jumpcraft",
    "Omega Parkour",
    "45 Strafe Journey",
    "Bonus 11",
    "Hypixel Parkour Duels",
    "Hypixel Housing",
    "Dream Dating Simulator",
    ]

@tasks.loop(minutes = 30)
async def change_presence():
    await bot.change_presence(activity = discord.Game(name = random.choice(text)))

@tasks.loop(minutes = 1)
async def reset_dailies():
    if datetime.now().hour == 0 and datetime.now().minute == 0:
        #Change datetime.now().hour to 24
        db = sqlite3.connect('database.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        result = cursor.fetchall()
        for row in result:
            if row[6] == 0:
                cursor.execute(f"UPDATE users SET daily_streak = 0 WHERE id = {row[0]}")
            cursor.execute(f"UPDATE users SET has_claimed_daily = 0 WHERE id = {row[0]}")
        print("Dailies have been reset!")
        db.commit()
        cursor.close()
        db.close()

@change_presence.before_loop
@reset_dailies.before_loop
async def before():
    await bot.wait_until_ready()

for file in os.listdir("commands/"):
    if file == "__pycache__":
        continue
    else:
        bot.load_extension(f"commands.{file[:-3]}")


change_presence.start()
reset_dailies.start()
bot.run(TOKEN)