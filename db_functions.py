import sqlite3
import discord

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

async def get_shop_item_index(index):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT name FROM shop")
    result = cursor.fetchall()

    if result is None:
        return None
    name = result[(index)]
    cursor.execute(f"SELECT price FROM shop")
    price = cursor.fetchall()[index]
    cursor.execute(f"SELECT level_req FROM shop")
    level_req = cursor.fetchall()[index]
    cursor.execute(f"SELECT emoji FROM shop")
    emoji = cursor.fetchall()[index]
    cursor.execute(f"SELECT description FROM shop")
    description = cursor.fetchall()[index]

    
    item = {}
    item['name'] = name[0]
    item['price'] = price[0]
    item['level_req'] = level_req[0]
    item['emoji'] = emoji[0]
    item['description'] = description[0]

    db.commit()
    cursor.close()
    db.close()
    return item

async def get_shop_item(item):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT name FROM shop WHERE name = '{item}'")
    result = cursor.fetchone()
    if result is None:
        return None

    cursor.execute(f"SELECT price FROM shop WHERE name = '{result[0]}'")
    price = cursor.fetchone()
    cursor.execute(f"SELECT level_req FROM shop WHERE name = '{result[0]}'")
    level_req = cursor.fetchone()
    cursor.execute(f"SELECT emoji FROM shop WHERE name = '{result[0]}'")
    emoji = cursor.fetchone()
    cursor.execute(f"SELECT description FROM shop WHERE name = '{result[0]}'")
    description = cursor.fetchone()

    
    item = {}
    item['name'] = result[0]
    item['price'] = price[0]
    item['level_req'] = level_req[0]
    item['emoji'] = emoji[0]
    item['description'] = description[0]

    db.commit()
    cursor.close()
    db.close()
    return item

async def add_item(id, item_name, amount, emoji, description, price):
    db = sqlite3.connect('database.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT amount FROM items WHERE id = {id} AND name = '{item_name}'")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO items(id, name, amount, emoji, description, price) VALUES(?,?,?,?,?,?)")
        val = (id, item_name, amount, emoji, description, price)
        cursor.execute(sql, val)
    else:
        cursor.execute(f"UPDATE items SET amount = {result[0] + amount} WHERE id = {id} AND name = '{item_name}'")
    cursor.execute("DELETE FROM items WHERE amount = 0")
    db.commit()
    cursor.close()
    db.close()
    return
