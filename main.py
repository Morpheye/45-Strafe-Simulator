import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import CommandOnCooldown
import sqlite3
import os
from dotenv import load_dotenv

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
        await ctx.send(f"You must wait **{error.retry_after:.2f}** seconds before doing this again, **{ctx.author}**")
        return
    raise error
 
@bot.event
async def on_ready():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    print(f"Logged in as {bot.user}!")

#commands
for file in os.listdir("commands/"):
    bot.load_extension(f"commands.{file[:-3]}")

bot.run(TOKEN)

