import discord
import configparser
import re
from pymongo import MongoClient
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
    if message.author == client.user:
        return

    if message.content == '!a help':
        await message.channel.send("Help not available!")

    if re.match(r"Wordle [0-9]+ [1-6|X]/6", message.content) is not None:
        # extract the Wordle number from message
        wordle = message.content.splitlines()[0].split(" ")[1]
        # extract the score from message
        score = message.content.splitlines()[0].split(" ")[2][0]

        await message.channel.send()


if __name__ == "__main__":
    config.read(ini_path)
    cluster = MongoClient(config.get("section", "mongo_url"))

    collection = cluster["wordle"]["data"]

    s = collection.find_one({"_id": ObjectId("62a7d0a9a2559438d2907f0e")})
    print(s)

    client.run(config.get("section", "token"))
