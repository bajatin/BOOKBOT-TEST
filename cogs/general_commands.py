import discord
from discord.ext import commands
import requests
import re
import json
import asyncio

class General_commands(commands.Cog):
  def __init__(self,client):
    self.client =  client
  
  @commands.Cog.listener()
  @commands.has_permissions(manage_roles=True, manage_messages=True)
  async def on_message(self, message):
      if message.guild is None:
        if message.author != self.client.user:
          pass


      else:
          if message.guild.id == 584581061271617538:
              if message.author.bot:
                  pass  
              else:
                  role = message.guild.get_role(595403641058492416)
                  if role not in message.author.roles:
                      if re.search("knowledge is power",message.content,re.IGNORECASE):          
                          await message.author.add_roles(role)
                          embed = discord.Embed(title="Welcome Reader :book:",description=f"{message.author.mention} you now have the reader role. Feel free to explore the server.")
                          await message.channel.send(embed=embed)
                          await message.delete()
          
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
  

  @commands.command(brief="ping the bot", description="ping the bot")
  async def ping(self,ctx):
      await ctx.send("Pong!")


  @commands.command(brief="pong the bot", description="pong the bot")
  async def pong(self,ctx):
      await ctx.send("Ping!")
def setup(client):
  client.add_cog(General_commands(client))