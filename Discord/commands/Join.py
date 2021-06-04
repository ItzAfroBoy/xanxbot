import logging
import discord
from discord.ext import commands


class Join(commands.Cog):

    def __init__(self, client):
        self.client = client

    version = '1.0.0'

    @commands.command()
    @commands.has_role('@everyone')
    async def join(self, ctx: commands.Context, member: discord.Member = None):
        member = ctx.author

        if ctx.channel.id == 720809487157690461:

            await member.add_roles()
            await member.send(f'Welcome to {ctx.guild.name}. Please read the rules')
            logs.info(f'{member} has joined {ctx.guild.name}')


logs = logging.getLogger('bot')


def setup(client):
    client.add_cog(Join(client))
