import time
import asyncio
import discord
import random
from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    version = '1.0.3'

    @commands.Cog.listener()
    async def on_ready(self):
        self.x = self.client.get_cog('Utils')

    @commands.command()
    async def gif(self, ctx):
        """ Get a random GIF """
        gif = random.choice(self.x.gifs)
        await ctx.send(f'Here you go\n{gif}')

    @commands.command()
    async def calc(self, ctx, numOne: int, op, numTwo: int):
        """ Do simple calculations """
        if op == '+':
            embed = discord.Embed(
                title=f'Answer: {numOne + numTwo}', color=self.x.color())
            await ctx.send(embed=embed)
        elif op == '-':
            embed = discord.Embed(
                title=f'Answer: {numOne - numTwo}', color=self.x.color())
            await ctx.send(embed=embed)
        elif op == 'x':
            embed = discord.Embed(
                title=f'Answer: {numOne * numTwo}', color=self.x.color())
            await ctx.send(embed=embed)
        elif op == '/':
            embed = discord.Embed(
                title=f'Answer: {numOne / numTwo}', color=self.x.color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='You what?', color=self.x.color())
            embed.add_field(name='Operators:', value='+')
            embed.add_field(name='\t', value='-')
            embed.add_field(name='\t', value='x')
            embed.add_field(name='\t', value='/')
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        


def setup(client):
    client.add_cog(Commands(client))
