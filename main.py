import discord
from discord.ext import commands

import configparser
import datetime
import re

from pymongo import MongoClient
import pymongo.errors
from bson import ObjectId

description = '''Wordle Bot'''

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents, help_command=None)

config = configparser.ConfigParser()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='help')
async def _help(ctx):
    await ctx.send(f"Help not available!")


@bot.command(name='score', pass_context=True)
async def _score(ctx):
    total = []
    total_score = 0

    cursor = collection.find({
        "username": ctx.message.author.name
    })
    for index, doc in enumerate(cursor):
        total.append(
            {
                "username": doc["username"],
                "game_score": doc["game_score"]
            }
        )

    for dict_item in total:
        for key in dict_item:
            if dict_item[key].isdigit():
                total_score += int(dict_item[key])

    await ctx.message.channel.send(f"Your total Wordle score is ``{total_score}``", reference=ctx.message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if re.match(r"Wordle [0-9]+ [1-6|X]/6", message.content) is not None:
        wordle = message.content.splitlines()[0].split(" ")[1]
        score = message.content.splitlines()[0].split(" ")[2][0]

        if collection.find_one({
            "username": message.author.name,
            "game_num": wordle,
        }):
            await message.channel.send(f"Can't add wordle score again for today!",
                                       reference=message)
            return

        try:
            collection.insert_one(
                {
                    "_id": message.id,
                    "username": message.author.name,
                    "game_num": wordle,
                    "game_score": score,
                    "date": datetime.datetime.now()
                }
            )
        except pymongo.errors.DuplicateKeyError:
            await message.channel.send("Duplication not allowed!", reference=message)
            return

        await message.channel.send("Record submitted!", reference=message)

    await bot.process_commands(message)


if __name__ == "__main__":
    ini_path = 'token.ini'
    config.read(ini_path)

    cluster = MongoClient(config.get("section", "mongo_url"))
    collection = cluster["wordle"]["data"]

    bot.run(config.get("section", "token"))
