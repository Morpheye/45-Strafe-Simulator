import discord
from discord.ext import commands
from db_functions import add_coins, get_level, get_coins, get_kriddytoo_shrine_boost, add_kriddytoo_shrine_boost, get_shop_item, add_item

@commands.command(name = "buy", aliases = ["purchase"], description = "Buy an item from the shop")
@commands.bot_has_permissions(send_messages=True)
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy(ctx, choice="null"):

    if await get_level(ctx.author.id) < 2:
        return await ctx.send(f"**{ctx.author}**, buying items requires **level 2**")

    if choice == "null":
        return await ctx.send(f"**{ctx.author}**, please specify an item to purchase")

    item = await get_shop_item(choice)
    if item is None:
        return await ctx.send(f"**{ctx.author}**, that item is not in the shop!")
    
    if await get_level(ctx.author.id) < item['level_req']:
        return await ctx.send(f"**{ctx.author}**, you are not high enough level to buy that item! \nLevel: **{await get_level(ctx.author.id)} / {item['level_req']}**")

    if await get_coins(ctx.author.id) < item['price']:
        return await ctx.send(f"**{ctx.author}**, you cannot afford that item! \nCoins missing: **{item['price'] - await get_coins(ctx.author.id)}** :coin:")

    await add_item(ctx.author.id, item['name'], 1, item['emoji'], item['description'])
    await add_coins(ctx.author.id, (-1 * item['price']))

    await ctx.send(f"**{ctx.author}**, you successfully purchased **{item['name']}** for **{item['price']}** :coin:")


def setup(bot):
    bot.add_command(buy)
