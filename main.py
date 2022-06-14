import discord
import configparser
import re

from pymongo import MongoClient
import pymongo.errors
import datetime
from bson import ObjectId

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)
config = configparser.ConfigParser()
ini_path = 'token.ini'


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    total = []
    total_score = 0

    if message.author == client.user:
        return

    if message.content == '!w help':
        await message.channel.send("Help not available!")

    if message.content == '!w score':
        cursor = collection.find({
            "username": message.author.name
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

        await message.channel.send(f"Your total Wordle score is ``{total_score}``", reference=message)

    if re.match(r"Wordle [0-9]+ [1-6|X]/6", message.content) is not None:
        wordle = message.content.splitlines()[0].split(" ")[1]
        score = message.content.splitlines()[0].split(" ")[2][0]

        if collection.find_one({
            "username": message.author.name,
            "game_num": wordle,
        }):
            await message.channel.send(f"Can't add wordle score again for today!",
                                       reference=message)
            return True

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
            return True

        await message.channel.send("Record submitted!", reference=message)


if __name__ == "__main__":
    config.read(ini_path)

    cluster = MongoClient(config.get("section", "mongo_url"))
    collection = cluster["wordle"]["data"]

    client.run(config.get("section", "token"))
