import random
import asyncio
import discord
from discord.ext import commands


class Storage(commands.Cog):

    def __init__(self, client):
        self.client = client

    def color(self):
        colors = []
        for _i in range(6):
            colors.append(random.choice('ABCDEF1234567890'))
        r = ''.join(colors)
        r = f"0x{r}"
        return int(r, base=16)

    async def GetMessage(self, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100):
        embed = discord.Embed(
            title=f"{contentOne}",
            description=f"{contentTwo}",
        )
        await ctx.send(embed=embed)
        try:
            msg = await self.client.wait_for(
                "message",
                timeout=timeout,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                return msg.content
        except asyncio.TimeoutError:
            return False

    gifs = ['https://media.giphy.com/media/IcifS1qG3YFlS/giphy.gif',
            'https://media.giphy.com/media/XIqCQx02E1U9W/giphy.gif',
            'https://media.giphy.com/media/85p0dpfRvPnfa/giphy.gif',
            'https://media.giphy.com/media/6qdKZFhT0VBm0/giphy.gif',
            'https://media.giphy.com/media/lfRP9MHSbr5kY/giphy.gif',
            'https://media.giphy.com/media/cvlM2nbg3ZalW/giphy.gif',
            'https://media.giphy.com/media/4jiMPuzeG09Ko/giphy.gif',
            'https://media.giphy.com/media/YfvZzNYOw5niM/giphy.gif',
            'https://media.giphy.com/media/h30Uk86LypXpe/giphy.gif',
            'https://media.giphy.com/media/c1ORoB1FORyqk/giphy.gif',
            'https://media.giphy.com/media/O2lPwWUO53lrG/giphy.gif',
            'https://media.giphy.com/media/vC5UDnWdwn5WU/giphy.gif',
            'https://media.giphy.com/media/19ekgONJcfYOc/giphy.gif',
            'https://media.giphy.com/media/qY0Po5kBnMNig/giphy.gif',
            'https://media.giphy.com/media/dfXFDTqtFCCDS/giphy.gif',
            'https://media.giphy.com/media/JzOyy8vKMCwvK/giphy.gif',
            'https://media.giphy.com/media/eoxomXXVL2S0E/giphy.gif',
            'https://media.giphy.com/media/Lswx7eb3gvxte/giphy.gif',
            'https://media.giphy.com/media/pladQGQugCvXG/giphy.gif',
            'https://media.giphy.com/media/11Nsw7vHY8i7pC/giphy.gif',
            'https://media.giphy.com/media/xUA7b2S7SxhM1cGdsQ/giphy.gif',
            'https://media.giphy.com/media/QP8fegBndjeb1vI6lP/giphy.gif',
            'https://media.giphy.com/media/5xtDarobRW68tNCgjUA/giphy.gif']

    botLink = 'https://discord.com/api/oauth2/authorize?client_id=845734001054449684&permissions=8&scope=bot'

    logChannel = 736568409973587978

    version = '1.0.0'

def setup(client):
    client.add_cog(Storage(client))
