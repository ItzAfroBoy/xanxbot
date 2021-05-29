from os import name
import time
import discord
import platform
from discord.ext import commands


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    version = '1.0.0'

    @commands.Cog.listener()
    async def on_ready(self):
        self.x = self.client.get_cog('Utils')

    @commands.group()
    async def info(self, ctx):
        """Info about the Bot"""
        if ctx.invoked_subcommand == None:
            owner = self.client.get_user(self.client.owner_id)

            embed = discord.Embed(
                title=f"{self.client.user.name}'s info", color=self.x.color())
            embed.add_field(
                name='ID:', value=self.client.user.id, inline=False)
            embed.add_field(name='Owner:', value=owner.mention, inline=False)
            embed.add_field(name='Commands:', value=len(self.client.commands))
            embed.add_field(name='Platform:',
                            value=platform.system(), inline=False)
            embed.add_field(name='Language:',
                            value=platform.python_implementation())
            embed.add_field(name='Library:', value='discord.py w/voice')
            embed.add_field(name='Guilds in:', value=len(
                self.client.guilds), inline=False)
            embed.add_field(name='Account created:',  value=self.client.user.created_at.strftime(
                "%H:%M UTC - %a, %d %B %Y"))
            embed.add_field(name='Library version:',
                            value=discord.__version__, inline=False)
            embed.add_field(name='Language version:',
                            value=platform.python_version())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text='Bot Info', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @info.command()
    async def user(self, ctx, member: discord.Member = None):
        """Info about a user in the server"""
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(
            title=f"{member.name}'s info", color=self.x.color())
        embed.add_field(name='ID:', value=member.id)
        embed.add_field(name='Bot', value=member.bot)
        embed.add_field(name='Status:', value=member.status)
        embed.add_field(name='Nickname:', value=member.display_name)
        embed.add_field(name=f'Roles ({len(roles)}):', value=' '.join(
            [role.name for role in roles]))
        embed.add_field(name='Account created', value=member.created_at.strftime(
            "%H:%M UTC - %a, %d %B %Y"))
        embed.add_field(name='Highest role:', value=member.top_role)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f'Requested by: {ctx.author}', icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @info.command()
    async def guild(self, ctx):
        """Info about the server"""
        guild = ctx.guild
        roles = [role for role in guild.roles]
        embed = discord.Embed(
            title=f'{guild.name} Guild Info', color=self.x.color())
        embed.add_field(name='ID:', value=guild.id)
        embed.add_field(name='Owner:', value=guild.owner)
        embed.add_field(name='Region:', value=guild.region)
        embed.add_field(name='Emojis:', value=len(guild.emojis))
        embed.add_field(name='Created:', value=guild.created_at.strftime(
            "%H:%M UTC - %a %d %b %Y"))
        embed.add_field(name=f'Roles ({len(roles)}):', value=', '.join(
            [role.name for role in roles]), inline=False)
        embed.add_field(name='Description:', value=guild.description)
        embed.add_field(name='Members (w/bots):', value=guild.member_count)
        embed.add_field(name='Special features:', value=len(guild.features))
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx, mode: int = 1):
        """ ==> Bot latency <== """
        if mode == 2:
            bf = time.monotonic()
            msg = await ctx.send("Pong! :ping_pong:")
            ping = (time.monotonic() - bf) * 1000
            await msg.edit(content=f'Pong! `{int(ping)}ms` :ping_pong:')
        else:
            await ctx.send(f"Pong! {int(self.client.latency * 1000)}ms :ping_pong:")

    # @commands.command()
    # async def help(self, ctx):
    #     member = ctx.author
    #     embed = discord.Embed(title='Help', color=self.x.color())
    #     embed.add_field(name='Prefix', value='::')
    #     embed.add_field(name='guild', value='Info about the server')
    #     embed.add_field(name='show', value='Info about a user in the server')
    #     embed.add_field(name='info', value='Info about the bot')
    #     embed.add_field(
    #         name='ping', value='Display the latency between Bot and Discord')
    #     embed.add_field(name='gif', value='Shows a shit selection of gifs')
    #     embed.set_author(name=self.client.user.mention)
    #     embed.set_footer(
    #         text=f'Requested by: {member}', icon_url=member.avatar_url)
    #     embed.set_thumbnail(url='https://i.ibb.co/rMrRx5S/Help.png')


def setup(client):
    client.add_cog(Info(client))
