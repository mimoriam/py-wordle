import discord
import configparser
import re

import pymongo.errors
from pymongo import MongoClient
from bson import ObjectId
import datetime

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
    if message.author == client.user:
        return

    if message.content == '!a help':
        await message.channel.send("Help not available!")

    if re.match(r"Wordle [0-9]+ [1-6|X]/6", message.content) is not None:
        wordle = message.content.splitlines()[0].split(" ")[1]
        score = message.content.splitlines()[0].split(" ")[2][0]

        if collection.find_one({
            "username": message.author.name,
            "game_num": wordle,
            "game_score": score
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
        except pymongo.errors.DuplicateKeyError as e:
            await message.channel.send("Duplication not allowed!", reference=message)
            return

        await message.channel.send("Record submitted!", reference=message)


if __name__ == "__main__":
    config.read(ini_path)
    cluster = MongoClient(config.get("section", "mongo_url"))

    collection = cluster["wordle"]["data"]

    client.run(config.get("section", "token"))
