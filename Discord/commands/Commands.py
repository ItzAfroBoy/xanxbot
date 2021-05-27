import time
import asyncio
import discord
import random
from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.s = self.client.get_cog('Storage')

    version = '1.0.0'

    @commands.command()
    async def gif(self, ctx):
        gif = random.choice(self.s.gifs)
        await ctx.send(f'Here you go\n{gif}')

    @commands.command()
    async def calc(self, ctx, numOne: int, op, numTwo: int):
        if op == '+':
            embed = discord.Embed(
                title=f'Answer: {numOne + numTwo}', color=self.s.color())
            await ctx.send(embed=embed)
        elif op == '-':
            embed = discord.Embed(
                title=f'Answer: {numOne - numTwo}', color=self.s.color())
            await ctx.send(embed=embed)
        elif op == 'x':
            embed = discord.Embed(
                title=f'Answer: {numOne * numTwo}', color=self.s.color())
            await ctx.send(embed=embed)
        elif op == '/':
            embed = discord.Embed(
                title=f'Answer: {numOne / numTwo}', color=self.s.color())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='You what?', color=self.s.color())
            embed.add_field(name='Operators:', value='+')
            embed.add_field(name='\t', value='-')
            embed.add_field(name='\t', value='x')
            embed.add_field(name='\t', value='/')
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
