import logging
import math
from os import name
import sqlite3 as sql3
import time

import discord
from discord.ext import commands


class Leveling(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.x = client.get_cog('Utils')

    version = '1.2.1'

    @commands.Cog.listener()
    async def on_ready(self):
        self.x = self.client.get_cog('Utils')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            pass
        else:
            db = sql3.connect(r'.\data\leaderboard.db')
            cur = db.cursor()
            cur.execute(
                f'SELECT user_id FROM levels WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}')
            res = cur.fetchone()
            if not res:
                sql = (
                    "INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
                val = (message.guild.id, message.author.id, 1, 1)
                cur.execute(sql, val)
                db.commit()
            else:
                cur.execute(
                    f'SELECT user_id, exp, lvl FROM levels WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}')
                res1 = cur.fetchone()
                xp = res1[1]
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? AND user_id = ?")
                val = (xp + 1, message.guild.id, message.author.id)
                cur.execute(sql, val)
                db.commit()

                cur.execute(
                    f'SELECT user_id, exp, lvl FROM levels WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}')
                res2 = cur.fetchone()

                xp_start = res2[1]
                lvl_start = res2[2]
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start / 2)
                if xp_start > xp_end:
                    await message.author.send(f'Hey! You are now level {lvl_start + 1} in {message.guild.name}')
                    sql = (
                        "UPDATE levels SET lvl = ? WHERE guild_id = ? AND user_id = ?")
                    val = (lvl_start + 1, message.guild.id, message.author.id)
                    cur.execute(sql, val)
                    db.commit()
                    sql = (
                        "UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                    val = (0, message.guild.id, message.author.id)
                    cur.execute(sql, val)
                    db.commit()
                    cur.close()
            db.close()

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        """ Rank info of the user that calls it or someone in the guild """
        if not member:
            db = sql3.connect(r'.\data\leaderboard.db')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            res = cursor.fetchone()
            if not res:
                await ctx.send('You are not ranked yet')
            else:
                xp = res[1]
                lvl = res[2]
                xp_end = math.floor(5 * (lvl ^ 2) + 50 * lvl / 2)

                embed = discord.Embed(
                    title=f'Your level info!!', color=self.x.color())

                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name='Your Level:', value=lvl)
                embed.add_field(name='Your XP:', value=xp+1)
                embed.set_footer(
                    text=f'XP till next level: {xp_end - xp - 1}')
                await ctx.send(embed=embed)
            cursor.close()
        else:
            db = sql3.connect(r'.\data\leaderboard.db')
            cur = db.cursor()
            cur.execute(
                f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = {ctx.guild.id} and user_id = {member.id}")
            res = cur.fetchone()
            if not res:
                await ctx.send("That user is not ranked")
            else:
                xp = res[1]
                lvl = res[2]
                xp_end = math.floor(5 * (lvl ^ 2) + 50 * lvl / 2)

                embed = discord.Embed(
                    title=f'{member.name} level info!!', color=self.x.color())

                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name='Your Level:', value=lvl)
                embed.add_field(name='Your XP:', value=xp+1)
                embed.set_footer(
                    text=f'XP till next level: {xp_end - xp - 1}')
                await ctx.send(embed=embed)
            cur.close()
        db.close()

    @commands.group()
    async def ranks(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send('Please specify server or all servers: ::ranks server or ::ranks all')

    @ranks.command()
    async def guild(self, ctx, member: discord.User = None):
        "Ranking of the guild this command is called in"
        db = sql3.connect(r'.\data\leaderboard.db')
        cur = db.cursor()
        cur.execute(
            f'SELECT user_id, exp, lvl FROM levels WHERE guild_id = {ctx.guild.id}')
        res = cur.fetchall()
        if not res:
            await ctx.send('Uhhh ... What?')
            logs.error(
                'Something is wrong when fetching results from the database. Called on `rank server` command')
        else:
            x = 0
            embed = discord.Embed(
                title=f"{ctx.guild.name}'s leaderboard", color=self.x.color())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'{time.strftime("%H:%M:%S - %a %d %b")}')
            for i in res:
                x += 1
                member = self.client.get_user(int(i[0]))
                if not member:
                    pass
                else:
                    embed.add_field(
                        name=f'{x}. {member.name}', value=f'Level {i[2]} : {i[1]}xp', inline=False)
            await ctx.send(embed=embed)
            cur.close()
        db.close()

    @ranks.command()
    async def all(self, ctx, mode: str = None):
        """ Ranking that includes info from all guilds """
        res = self.x.sort(mode)
        if not res:
            await ctx.send('Something went wrong')
            logs.error('Cannot fetch results')
        else:
            x = 0
            embed = discord.Embed(
                title="Global leaderboard", color=self.x.color())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'{time.strftime("%H:%M:%S - %a %d %b")}')
            for i in res:
                x += 1
                try:
                    member = await self.client.fetch_user(int(i[0]))
                    embed.add_field(
                        name=f'{x}. {member.name}', value=f'Level {i[2]} : {i[1]}xp ', inline=False)
                except:
                    pass
            await ctx.send(embed=embed)


logs = logging.getLogger('bot')


def setup(client):
    client.add_cog(Leveling(client))
