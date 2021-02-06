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
    resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
    result = resource.list(q=book_name, cx ='466efafd8a2c95b3b').execute()
    link = result['items'][0]['link']
    await ctx.send(link)
  
  @commands.command(brief='Sends the book details',description='Sends the book details')
  async def gr(self,ctx, *,book_name):
    resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
    result = resource.list(q=book_name, cx ='466efafd8a2c95b3b').execute()
    link = result['items'][0]['link']
    dets = await book_dets(link)
    with open('details.json', 'w+') as f:
        json.dump(dets, f, indent=4)
    with open('details.json', 'r') as f:
        details = json.load(f)
        the_embed = discord.Embed.from_dict(details)
        await ctx.send(embed=the_embed)

def setup(client):
  client.add_cog(Book_search(client))