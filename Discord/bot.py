import asyncio
import logging
import os

import discord
from discord.ext import commands
from discord.flags import Intents

import utils

__version__ = '1.1.0'

intents = Intents.default()
intents.members = True

client = commands.Bot(command_prefix='::', intents=intents)
# client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='The Bot || ::help', url="https://discord.gg/FkXPHuN", state='On Discord'))
    logs.info(f'Username |==> {client.user.name}')
    logs.info(f'ID |==> {client.user.id}')


@client.command()
@commands.is_owner()
async def enable(ctx, extention: str):
    client.load_extension(f'commands.{extention.capitalize()}')
    x = client.get_cog(extention.capitalize())
    logs.info(f'{extention} cog is now available @ version {x.version}')


@client.command()
@commands.is_owner()
async def disable(ctx, extention: str):
    x = client.get_cog(extention.capitalize())
    logs.info(f'{extention} cog has been removed @ version {x.version}')
    client.unload_extension(f'commands.{extention.capitalize()}')


@client.command()
@commands.is_owner()
async def reload(ctx, extention: str = None):
    if not extention:
        x = 0
        for f in os.listdir('./commands'):
            if f.endswith('.py'):
                client.reload_extension(f'commands.{f[:-3].capitalize()}')
                x += 1
        logs.info(f'All {x} cogs reloaded @ bot version {__version__}')
    else:
        client.reload_extension(f'commands.{extention.capitalize()}')
        x = client.get_cog(extention.capitalize())
        logs.info(
            f'{extention.capitalize()} cog has been reloaded @ version {x.version}')


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    logs.warn('Shutting Down...')
    await client.change_presence(activity=discord.Game('Going Dark'), status=discord.Status.dnd)
    asyncio.sleep(3)
    await client.close()

# ==> Logger <== #
logs = logging.getLogger('bot')
logs.setLevel(logging.DEBUG)
hand = logging.FileHandler(filename='./logs/bot.log',
                           encoding='utf-8', mode='w')
hand.setFormatter(logging.Formatter(
    '%(asctime)s :: %(levelname)s :: %(name)s: %(message)s'))
logs.addHandler(hand)

x = 0
for f in os.listdir('./commands'):
    if f.endswith('.py'):
        client.load_extension(f'commands.{f[:-3].capitalize()}')
        x += 1
logs.debug(f'All {x} cogs loaded successfully @ bot version {__version__}')

if __name__ == '__main__':
    client.run(utils.token)
