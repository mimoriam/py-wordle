import discord
import configparser
import re


intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)
config = configparser.ConfigParser()
ini_path = 'token.ini'


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


if __name__ == "__main__":
    config.read(ini_path)
    client.run(config.get('section', 'token'))
