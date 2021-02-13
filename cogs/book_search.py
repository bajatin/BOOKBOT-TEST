import discord
from discord.ext import commands
import os
from googleapiclient.discovery import build
from helper.get_book_dets import book_dets
import json

class Book_search(commands.Cog):

  def __init__(self, client):
    self.client =  client

  @commands.command(brief='Sends the goodreads link of the book',description='Sends the goodreads link of the book')
  async def grl(self, ctx, * ,book_name):
    async with ctx.typing():
      resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
      result = resource.list(q=book_name, cx ='466efafd8a2c95b3b').execute()
      if "items" in result:
        link = result['items'][0]['link']
      else:
        link = 'Good Job!  Even Google can\'t find this book on goodreads'
    # print(link)
    await ctx.send(link)


  @grl.error
  async def grlerror(self,ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="❌ Error",description= "I can't read minds you know. So.... \n if it's not too much trouble do you mind writing the book name too?",
  colour=16187392)
      await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="❌ Error",description='The bot is missing some permissions')
      await ctx.send(embed=embed)
    else:
      raise error

  @commands.command(brief='Sends the book details',description='Sends the book details')
  async def gr(self,ctx, *,book_name):
    async with ctx.typing():
      resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
      result = resource.list(q=book_name, cx ='466efafd8a2c95b3b').execute()
      if "items" in result:
        link = result['items'][0]['link']
        dets = await book_dets(link)
      else:
        dets = {'description':'Good Job!  Even Google can\'t find this book on goodreads'}
      with open('details.json', 'w+') as f:
          json.dump(dets, f, indent=4)
    with open('details.json', 'r') as f:
        details = json.load(f)
        the_embed = discord.Embed.from_dict(details)
        await ctx.send(embed=the_embed)

  @gr.error
  async def grerror(self,ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="❌ Error",description= "I can't read minds you know. So.... \n if it's not too much trouble do you mind writing the book name too?",colour=16187392)
      await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="❌ Error",description='The bot is missing some permissions')
      await ctx.send(embed=embed)
    else: 
      raise error

def setup(client):
  client.add_cog(Book_search(client))