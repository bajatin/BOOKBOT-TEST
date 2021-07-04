import os
from keep_alive import keep_alive
import discord
from discord.ext import commands
import traceback 
import datetime

client = commands.Bot(
	command_prefix="*",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

client.author_id = 702845167643787301  # Change to your discord id!!!

@client.event
async def on_error(event, *args, **kwargs):
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.datetime.utcnow()
    await client.get_channel(807570072406982657).send(embed=embed)

@client.event 
async def on_ready():  # When the client is ready
    await client.change_presence(status=discord.Status.online, activity=discord.Game(' with your time'))
    print(f"We logged in as {client.user}")


extensions = [
	'cogs.dev_commands',
  'cogs.book_search',
  'cogs.general_commands'
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		client.load_extension(extension)  # Loades every extension.

token = os.getenv("TOKEN") 
keep_alive()  # Starts a webserver to be pinged.

client.run(token)  # Starts the client