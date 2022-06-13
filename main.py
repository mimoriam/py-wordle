import discord
import configparser
import re

# https://discord.com/api/oauth2/authorize?client_id=864098900687192075&permissions=67584&scope=bot

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
