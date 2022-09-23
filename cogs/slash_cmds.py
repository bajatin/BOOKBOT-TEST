import discord
from discord.ext import commands
import os
from googleapiclient.discovery import build
from helper.get_book_dets import book_dets
from dislash import *
import re
from helper.cal_hob import get_link

class Slash_cmds(commands.Cog):

  def __init__(self, client):
    self.client =  client

  @slash_commands.command(name='calvin',description='Sends a random calvin and hobbes comic',guild_ids= [805042403441639455,584581061271617538])
  async def callink(self, ctx):
    # async with ctx.typing():
      await ctx.reply(type=5)
      [link, year, month, day] = get_link()
      title = f"Calvin Hobbes Issue On: {day}/{month}/{year}\n"
      embed = discord.Embed(title = title)
      embed.set_image(url=link)
      await ctx.edit(embed=embed)

  @slash_commands.command(description='Sends the goodreads link of the book',guild_ids= [805042403441639455,584581061271617538],options=[Option("book_name","Enter book title",Type.STRING,required=True)])
  async def grl(self, ctx,*,book_name):
      await ctx.reply(type=5)
      resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
      result = resource.list(q=book_name, cx =os.getenv('CSE_ID')).execute()
      if "items" in result:
        link = result['items'][0]['link']
      else:
        link = 'Good Job!  Even Google can\'t find this book on goodreads'
      await ctx.edit(content=link)

  @slash_commands.command(description='Sends the goodreads data of the book',guild_ids= [805042403441639455,584581061271617538],options=[Option("book_name","Enter book title",Type.STRING,required=True)])
  async def gr(self,ctx, *,book_name):
      await ctx.reply(type=5)
      if re.match("https://www.goodreads.com/book/show/*",book_name):
        link = book_name
        dets = await book_dets(link)
      else:
          resource = build("customsearch", 'v1', developerKey =os.getenv('API_KEY') ).cse()
          result = resource.list(q=book_name, cx =os.getenv('CSE_ID')).execute()
          if "items" in result:
            link = result['items'][0]['link']
            dets = await book_dets(link)
          else:
            dets = {'description':'Good Job!  Even Google can\'t find this book on goodreads'}
      the_embed = discord.Embed.from_dict(dets)
      await ctx.edit(embed=the_embed)

def setup(client):
  client.add_cog(Slash_cmds(client))