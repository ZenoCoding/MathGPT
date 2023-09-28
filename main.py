import asyncio
from aiohttp.client_exceptions import ClientConnectorError
import os
import openai
import logging

import discord

import utils

logging.basicConfig(filename='discord.log', encoding='utf-8', level=logging.INFO)

# create logger
logger = logging.getLogger('MathGPT')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('[%(asctime)s - %(levelname)s]: [%(name)s] %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Discord Initialization
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')


@bot.slash_command(name='help', description='Receive some assistance!',
                   guilds=[discord.Object(id=os.environ.get("DISCORD_ID"))])
async def help_command(interaction: discord.Interaction):
    embed = utils.create_embed(title="Command Help", description="Here are the commands you can use with MathGPT!")
    embed.add_field(name="help", value="Receive some assistance!", inline=False)
    await interaction.response.send_message(embed=embed)


# Cog loader
cogs = [file[:-3] for file in os.listdir('cogs') if file.endswith('.py')]
logger.info(f'Loading {len(cogs)} cogs...')
try:
    for cog in cogs:
        bot.load_extension(f'cogs.{cog}')
except ClientConnectorError as e:
    logger.error("Error connecting to discord's servers, attempting again in 30 seconds.")
    delay = 30
    while True:
        asyncio.sleep(delay)
        try:
            for cog in cogs:
                bot.load_extension(f'cogs.{cog}')
        except ClientConnectorError as e:
            logger.error(
                "Reconnect failed. Now attempting to reconnect every 5 minutes." if delay == 30 else "Reconnect failed.")
            delay = 600
        else:
            logger.error("Reconnect and loading of cogs successful!")
            break

logger.info('All cogs loaded!')

bot.run('')
