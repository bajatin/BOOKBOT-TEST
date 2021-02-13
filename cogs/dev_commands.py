import discord
from discord.ext import commands


class DevCommands(commands.Cog, name='Developer Commands'):
  def __init__(self, bot):
    self.bot = bot
    self.channel = bot.get_channel(807570072406982657)

  async def cog_check(self, ctx):  
    return ctx.author.id == self.bot.author_id

  @commands.command(name='reload',aliases=['rl'])
  async def reload(self, ctx, cog):
    extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
    if cog == 'all':  # Lets you reload all cogs at once
      for extension in extensions:
        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
      await ctx.send('Cogs Reloaded')
    if cog in extensions:
      self.bot.unload_extension(cog)  # Unloads the cog
      self.bot.load_extension(cog)  # Loads the cog
      await ctx.send('Reloaded cog(s)')  # Sends a message where content='Done'
    else:
      await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

  @commands.command(name="unload", aliases=['ul']) 
  async def unload(self, ctx, cog):
    extensions = self.bot.extensions
    if cog not in extensions:
      await ctx.send("Cog is not loaded!")
      return
    self.bot.unload_extension(cog)
    await ctx.send(f"`{cog}` has successfully been unloaded.")

  @commands.command(name="load")
  async def load(self, ctx, cog):
    try:
      self.bot.load_extension(cog)
      await ctx.send(f"`{cog}` has successfully been loaded.")
    
    except commands.errors.ExtensionNotFound:
      await ctx.send(f"`{cog}` does not exist!")

  @commands.command(name="listcogs", aliases=['lc'])
  async def listcogs(self, ctx):
    base_string = "```css\n"  # Gives some styling to the list (on pc side)
    base_string += "\n".join([str(cog) for cog in self.bot.extensions])
    base_string += "\n```"
    await ctx.send(base_string)

  @commands.command()
  async def announce(self,ctx, *,arg):
    embed = discord.Embed(title='UPDATE',description=arg,colour=261327)
    channel = self.bot.get_channel(804867388302426132)
    await channel.send(embed= embed)

  @commands.command()
  async def listch(self,ctx):
    guild = self.bot.get_channel(804867388302426132)
    await ctx.send(guild)


def setup(bot):
  bot.add_cog(DevCommands(bot))