import json
import discord
from discord.ext import commands
path = __file__.replace("/cogs/cogs.py","")

with open(f'{path}/storage/main.json', 'r') as js:
  data = json.load(js)
class Example(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, message):

#emblem and test server here
    try:
      if message.guild.id != 0:
        #Custom commands
        if message.content.lower() in data["Custom_commands"].keys():
          await message.channel.send(data["Custom_commands"][message.content.lower()])
        else:
          #Banned sites prevention
          for i in data["banned_sites"]:
            for n in message.content.split():
              if n.startswith(i) or n.endswith(i):
                await message.channel.send(f'{message.author.name}#{message.author.discriminator} you have been warned for sending explicit content,ip grabbers or onion sites link')
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name='Muted'))
                await message.delete()
                break           
        #Bad words prevention
        if message.guild.id != 0:
          for i in message.content.split():
            if i.lower() in data["banned_words"]:
              await message.channel.send(f'{message.author.name}#{message.author.discriminator} you are warned not to speak foul words again')
              await message.delete()
              break  
    except:
      print('problem I dont care about')
    
      
def setup(client):
  client.add_cog(Example(client))

  #member.guild.id takes out the server id
		#if you have a problem just see what what tags are there in the variable for example in this case member
		#and according to the tags find out how to setitup for example message.guild.name like that