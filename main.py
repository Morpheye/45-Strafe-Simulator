import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import CommandOnCooldown
import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()
#environment variables

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = "?", intents = discord.Intents.all(), activity = discord.Game(name = "MCPK"))
bot.remove_command('help')

async def add_user(id):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    sql = ("INSERT INTO users(id, coins) VALUES(?,?)")
    val = (id, 0)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    
async def add_coins(id, coins):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT coins FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    sql = ("UPDATE users SET coins = ? WHERE id = ?")
    val = (result[0] + coins, id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def add_xp(id, xp, ctx):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT xp FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    
    #change xp
    sql = ("UPDATE users SET xp = ? WHERE id = ?")
    val = (result[0] + xp, id)
    cursor.execute(sql, val)

    #check if levelup
    current_xp = result[0] + xp
    cursor.execute(f"SELECT level FROM users WHERE id = {id}")
    current_level = cursor.fetchone()

    level_up_req = (10 * (current_level[0] ** 2)) + (1000 * current_level[0]) + 100

    if current_xp >= (level_up_req):
        sql = ("UPDATE users SET xp = ? WHERE id = ?")
        val = (current_xp - (level_up_req), id)
        cursor.execute(sql, val)

        sql = ("UPDATE users SET level = ? WHERE id = ?")
        val = (current_level[0] + 1, id)
        cursor.execute(sql, val)

        em = discord.Embed(title = "Level up!", description = f"**{ctx.author}**, you leveled up to level **{current_level[0] + 1}**", color = ctx.author.color)
    
        #level up message

        cursor.execute(f"SELECT message FROM levelupmessages WHERE level = {current_level[0] + 1}")
        message = cursor.fetchone()
        if message is not None:
            em.add_field(name = f"Level {current_level[0] + 1} rewards", value = message[0])

        await ctx.send(embed = em)


    db.commit()
    cursor.close()
    db.close()

async def get_coins(id):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT coins FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    cursor.execute(f"SELECT coins FROM users WHERE id = {id}")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result[0]

async def get_xp(id):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT xp FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    cursor.execute(f"SELECT xp FROM users WHERE id = {id}")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result[0]

async def get_level(id):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT level FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    cursor.execute(f"SELECT level FROM users WHERE id = {id}")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result[0]

async def get_kriddytoo_shrine_boost(id):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT kriddytoo_shrine_boost FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    cursor.execute(f"SELECT kriddytoo_shrine_boost FROM users WHERE id = {id}")
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result[0]

async def add_kriddytoo_shrine_boost(id, amount):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT kriddytoo_shrine_boost FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result is None:
        await add_user(id)
    sql = ("UPDATE users SET kriddytoo_shrine_boost = ? WHERE id = ?")
    val = (result[0] + amount, id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

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
bot.load_extension('commands.help')
bot.load_extension('commands.info')
bot.load_extension('commands.profile')
bot.load_extension('commands.test')

bot.load_extension('commands.single45')
bot.load_extension('commands.double45')
bot.load_extension('commands.triple45')
bot.load_extension('commands.pray')

bot.run(TOKEN)
