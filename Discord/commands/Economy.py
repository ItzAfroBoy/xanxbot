from discord.ext import commands

class Economy(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	verison= '1.0.0'

def setup(client):
	client.get_cog(Economy(client))