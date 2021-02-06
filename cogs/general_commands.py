import discord
from discord.ext import commands
import requests
import json

class General_commands(commands.Cog):
  def __init__(self,client):
    self.client =  client
  
  @commands.command(brief='Sends an inspirational quote',description='Sends an inspirational quote')
  async def inspire(self, ctx):
      try:
          response = requests.get("https://zenquotes.io/api/random")
      except requests.exceptions.HTTPError as errh:
          await ctx.send("An Http Error occurred:" + repr(errh))
      except requests.exceptions.ConnectionError as errc:
          await ctx.send("An Error Connecting to the API occurred:" + repr(errc))
      except requests.exceptions.Timeout as errt:
          await ctx.send("A Timeout Error occurred:" + repr(errt))
      except requests.exceptions.RequestException as err:
          await ctx.send("An Unknown Error occurred" + repr(err))
      else:
          data = json.loads(response.text)
          quote = data[0]['q'] + "\n -" + data[0]['a']
          embed = discord.Embed(title="Here to inspire 🌈", description= quote)
          await ctx.send(embed=embed)

def setup(client):
  client.add_cog(General_commands(client))