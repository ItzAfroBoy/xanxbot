from discord.ext import commands


class Giveaway(commands.Cog):

    def __init__(self, client):
        self.client = client

    version = '1.0.0'


def setup(client):
    client.get_cog(Giveaway(client))
