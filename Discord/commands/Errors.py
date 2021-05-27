import logging
from discord.ext import commands

class Errors(commands.Cog):

	def __init__(self, client):
		self.client = client

	version = '1.0.0'

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		owner = self.client.get_user(self.client.owner_id)
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Sorry! You haven't included all the required arguments!")
		elif isinstance(error, commands.MissingAnyRole):
			await ctx.send("Sorry! You don't have the permissions to use this")			
		elif isinstance(error, commands.CommandNotFound):
			await ctx.send("Sorry! That command doesn't exist")
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send("Sorry! Please wait before using this command again")
		elif isinstance(error, commands.ArgumentParsingError):	
			await ctx.send("Sorry! You have entered an incompatible argument")
		elif isinstance(error, commands.TooManyArguments):
			await ctx.send("Sorry! You have entered to many arguments")
		elif isinstance(error, commands.NotOwner):
			await ctx.send(f"Sorry! You aren't {owner.mention}")
		else:
			logs.error(error)

logs = logging.getLogger('bot')

def setup(client):
	client.add_cog(Errors(client))