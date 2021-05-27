import logging
import discord
from discord.ext import commands


class Mods(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.s = self.client.get_cog('Storage')

    version = '1.0.0'

    @commands.command()
    @commands.has_any_role('Druglord', 'Mods')
    async def clear(self, ctx, amount: int = 100):
        delete = await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{len(delete)} messages deleted :hamburger:', delete_after=2)

    @commands.command()
    @commands.has_any_role('Druglord', 'Mods')
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        await member.kick(reason=reason)
        logs.info(
            f'{member} kicked from {ctx.guild.name} for {reason or "unkown reason"}')

    @commands.command()
    @commands.has_any_role('Druglord', 'Mods')
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        await member.ban(reason=reason)
        logs.info(
            f'{member} banned from {ctx.guild.name} for {reason or "unkown reason"}')

    @commands.group()
    @commands.has_any_role('Druglord', 'Mods')
    async def give(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please specify what you want to give')

    @give.command()
    async def role(self, ctx, member: commands.MemberConverter, role: commands.RoleConverter):
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been given the role: {role}')
        logs.info(f'{member} has been given the role: {role}')

    @give.command()
    async def warning(self, ctx, member: commands.MemberConverter, *, warning: str = None):
        await ctx.send(f'{member.mention} has been warned for {warning or "an unknown reason"}')

    @give.command()
    async def botInvite(self, ctx: commands.Context, channel: discord.TextChannel = None, member: commands.MemberConverter = None):
        if not member:
            if not channel:
                await ctx.send('Please specify either a channel or member to send the bot link to')
            else:
                await channel.send(self.s.botLink)
        else:
            if not channel:
                await member.send(self.s.botLink)
                await ctx.send(f'The bot invite link has been sent to {member.mention}')
            else:
                await ctx.send("Doesn't make sense to send it to a channel and dm someone :smiley")

    @give.command()
    async def userInvite(self, ctx, member: commands.MemberConverter):
        invites = await ctx.guild.invites()
        await member.send(invites[0])
        await ctx.send(f'A user invite has been sent to {member.mention}')


logs = logging.getLogger('bot')


def setup(client):
    client.add_cog(Mods(client))
