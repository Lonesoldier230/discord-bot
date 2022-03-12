#made by Lone_soldier230
#import
import random
from discord.ext import commands,tasks
from discord import channel
import discord
import os
import path
import requests
import wikipedia
import json
import asyncio
from json.decoder import JSONDecodeError
import time
from googlesearch import search
#from dotenv import load_dotenv
#load_dotenv
#from keep_alive import keep_alive


#def
def color():
  #this program choose colors for the embed randomly
  color = (0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63
    ,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x607d8b,0x979c9f
    ,0x546e7a,0x7289da,0x99aab5)
  randclr = random.choice(color)
  return randclr


backup_data = {"TOKEN":None,"Prefix": None, "8ball": True, "Custom_commands": {"hello": "hi how are you"}, "kick_settings": {"kick": True, "text": "[admin] kicked [member]"}, "ban_settings": {"ban": True, "text": "[admin] banned [member]"}, "unban_settings": {"unban": True, "text": "[admin] unbanned [member]"}, "role_settings": {
    "role": True, "text": "[admin] has roled [member]"}, "unrole_settings": {"unrole": True, "text": "[admin] has unroled [member]"}, "mute_settings": {"mute": True, "text": "[member] has been muted by [admin]"}, "unmute_settings": {"unmute": True, "text": "[member] has been unmuted by [admin]"}, "insult": ["people clap when they see you.They clap their hands over their eyes.,you are proof that god has a sense of humour."
    , "you sir are the reason god created the middle finger."], "who_is": True, "randomn": True, "wikipedia": True,"google_search" : True,"banned_words":[""],"banned_sites":[""]}

#most essential program it finds where this file is located and changes dir here
path1 = path.__file__.replace('path.py', '')
paths = os.path.join(path1)
os.chdir(paths)


#this is where file is handeled
#config
for i in range(3):
  configurater = {0:"you made an error in main.json you have 60 seconds",1:"can you check main.json again you have 60 seconds"}
  try:
    with open('main.json','r') as js:
      data = json.load(js)
      break
  except JSONDecodeError as e:
    if i <2:
      print(configurater[i])
      time.sleep(60)
    else:
      print("""how many mistakes can you make idiot
figure that json file out and come and start this again""")
      exit()


print("Verifying...")
if data.keys() == backup_data.keys():
  print("Verified...")
else:
  backup_data.update(data)
  with open('main.json', 'w') as hson:
    json.dump(backup_data, hson, indent=4)
    data = dict(backup_data)

if data["TOKEN"] == None:
  print('pls enter your TOKEN')
  exit()
elif data["Prefix"] == None:
  print("pls enter the prefix")
  exit()

with open("who_is.json","r") as dicti:
    dictionary = json.load(dicti)


try:
  with open("mute_role.json" , "r") as mrj:
    Mute_roles = json.load(mrj)
except:
  print("hey dont mess with mute_role.json")

with open("google.json","r") as goog:
  gogle = json.load(goog)


#this is the brain of the bot
client = commands.Bot(command_prefix=data['Prefix'])
prefi = data['Prefix']
#body
@client.remove_command('help')
@client.command()
async def help(ctx,cate = None):
  embed = discord.Embed(title="Help", color= color())
  if cate == None:
    embed.add_field(name = "Moderator", value = f"`{prefi}help moderator/mod/commands`", inline = False)
    embed.add_field(name="Search", value=f"`{prefi}help search/look/google`", inline=False)
    embed.add_field(name="Fun", value=f"`{prefi}help fun`", inline=False)
  elif cate == "moderator" or cate == "mod" or cate == "commands":
    embed.add_field(name="Kick",value = f"`{prefi}kick <member> <reason>`",inline = False)
    embed.add_field(name="Ban",value = f"`{prefi}ban <member> <reason>`",inline = False)
    embed.add_field(name="Unban",value = f"`{prefi}unban <member#1234>`",inline = False)
    embed.add_field(name="Mute",value = f"`{prefi}mute <member>`",inline = False)
    embed.add_field(name="Unmute",value = f"`{prefi}unmute <member>`",inline = False)
    embed.add_field(name="Role",value = f"`{prefi}role <member> <role>`",inline = False)
  elif cate == "fun":
    embed.add_field(name='Insult',value = f"`{prefi}insult <member>`",inline = False)
    embed.add_field(name='Random',value = f"`{prefi}rand <max number>`",inline = False)
    embed.add_field(name='Who is set',value = f"`{prefi}who_is_set <your apithet>`",inline = False)
    embed.add_field(name='Who is',value = f"`{prefi}whois <user>`",inline = False)
  elif cate == "search" or cate == "look" or cate ==  "google":
    embed.add_field(name='Wikipedia',value = f"`{prefi}wiki or wikipedia <your question>`",inline = False)
    embed.add_field(name='Google',value = f"`{prefi}google or search <your question>`",inline = False)
  await ctx.send(embed=embed)

#this loads the config file
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

@client.event
async def on_ready():
  #to change activity and status of the bot
    await client.change_presence(status = discord.Status.do_not_disturb , activity = discord.Game(f'{prefi}help'))
    print('I am ready')

@client.event
async def on_member_join(member: discord.Member):
    print(f'{member.name} has joined')

@client.event
async def on_member_leave(member: discord.Member):
    print(f'{member.name} left the server')

@client.event
async def on_connect():
    print('connected to server')

@client.command()
async def ping(ctx, url = None):
  timeout = 1
  if url != None :
    try:
      request = requests.get(url , timeout=timeout)
      await ctx.send('the server is online')
    except:
      await ctx.send('the server is offline or doesnt exist')
  else:
    await ctx.send(f'pong {round(client.latency*1000)}ms')


@client.command(aliases=['8ball', 'roll'])
async def _8ball(ctx, *, questions=None):
  if data["8ball"] == True:
    if questions == None:
      embed = discord.Embed(
          title="8ball", description=".8ball <question>", color=color())
      await ctx.send(embed=embed)
    else:
      responses = ['probably', 'yes', 'no']
      await ctx.send(f'Question:{questions}\n Answer:{random.choice(responses)}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
  if data["kick_settings"]["kick"] == True:
    if user == None:
      embed = discord.Embed(title="Kick", description=f"`{prefi}kick <user> <reason>`", color=color())
      await ctx.send(embed=embed)
    else:
      if user.id == ctx.guild.me.id:
        await ctx.send("why are you trying to kick me")
      else:
        try:
          if ctx.author.top_role >user.top_role:
            await user.kick(reason=reason)
            if reason == None:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator} you better have a reason for this')
            else:
                await ctx.send(f"""{data["kick_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",reason)}""")
        except:
          await ctx.send(f"{user.name}#{user.discriminator} has a higher role then me")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
  if data["ban_settings"]["ban"] == True:
    if user == None:
      embed = discord.Embed(title="Ban", description=f"`{prefi}ban <user> <reason>`", color=color())
      await ctx.send(embed=embed)
    else:
      if user.id == ctx.guild.me.id:
        await ctx.send("why are you trying to ban me")
      else:
        try:
          if ctx.author.top_role > user.top_role:
            await user.ban(reason=reason)
            if reason == None:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator} you better have a reason for this')
            else:
                await ctx.send(f"""{data["ban_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",reason)}""")
        except:
          await ctx.send(f"{user.name}#{user.discriminator} has a higher role than me")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member=None):
  if data["unban_settings"]["unban"] == True:
    if member == None:
      embed = discord.Embed(title="Unban", description=f"`{prefi}unban <user>`", color=color())
      await ctx.send(embed=embed)
    else:
      banned_user = await ctx.guild.bans()
      member_name, member_discriminator = (member.split('#'))
      for BanEntry in banned_user:
          user = BanEntry.user
          if (user.name, user.discriminator) == (member_name, member_discriminator):
              await ctx.guild.unban(user)
              await ctx.send(f"""{data["unban_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")

@client.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, user: discord.Member = None, * ,role: discord.Role = None):
  if data["role_settings"]["role"] ==True:
    if user == None or role == None:
      embed = discord.Embed(title="Role", description=f"`{prefi}role <user> <role>`", color=color())
      await ctx.send(embed=embed)
    else:
      if ctx.author.top_role > role and ctx.guild.me.top_role > role:
        if role in user.roles:
          if data["unrole_settings"]["unrole"] == True:
            try:
                await user.remove_roles(role)
                await ctx.send(f"""{data["unrole_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
            except:
                print(os.error())
                try:
                    await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
                except Exception as e:
                    # if error
                    await ctx.send('There was an error running this command ')
                else:
                    await ctx.send(f"""{data["unrole_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
          else:
            await ctx.send(f"{user.name}#{user.discriminator} already has the role")
        else:
          try:
              await user.add_roles(role)
              await ctx.send(f"""{data["role_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
          except:
              print(os.error())
              try:
                  await user.add_roles(discord.utils.get(user.guild.roles, name=role))
              except Exception as e:
                    # if error
                  await ctx.send('There was an error running this command ')
              else:
                  await ctx.send(f"""{data["role_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
      elif ctx.author.top_role <= role:
        await ctx.send("your role is not high enough to give that role")
      elif ctx.guild.me.top_role <= role:
        await ctx.send("my role is not high enough")
      else:
        await ctx.send("sorry there was an error while executing the command")

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member = None, time:str = "None", *, reason=None):
  timing = {"s":1,"second":1,"seconds":1,"m":60 , "minute":60,"minutes":60 , "h":3600,"hour":3600 , "hours":3600, "d":86400,"day":86400,"days":86400}
  if data["mute_settings"]["mute"] == True:
    try:
      stc = Mute_roles[str(ctx.guild.id)]
      if user == None:
        embed = discord.Embed(title="Mute", description=f"`{prefi}mute <user>`", color=color())
        await ctx.send(embed=embed)
      else:
        Mute_rol = (discord.utils.get(user.guild.roles, name=f"{Mute_roles[str(ctx.guild.id)]}"))
        if user.id == ctx.guild.me.id:
          await ctx.send("why are you trying to mute me")
        else:
            if ctx.author.top_role > user.top_role and ctx.guild.me.top_role > user.top_role:
              if time != "None":
                for t in timing.keys():
                  if t in time:
                    try:
                      time = int(time.replace(t,""))
                      await user.add_roles(Mute_rol)
                      await ctx.send(f"""{data["mute_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",f"{reason}")}""")
                      await asyncio.sleep(timing[t]*time)
                      await user.remove_roles(Mute_rol)
                      break
                    except:
                      l = "no"
              else:
                l = "no"
              try:
                if l == "no":
                  if reason == None:
                    await user.add_roles(Mute_rol)
                    await ctx.send(f"""{data["mute_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",f"{time}")}""")
                  else:
                    await user.add_roles(Mute_rol)
                    await ctx.send(f"""{data["mute_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}").replace("[reason]",f"{time} {reason}")}""")
              except:
                return
            elif ctx.author.top_role <= user.top_role:
              await ctx.send("your role is not hght enough")
            elif ctx.guild.me.top_role <= user.top_role:
              await ctx.send("my role is not high enough")
            else:
              await ctx.send("sorry there was an error while executing the command")
    except KeyError as jsd:
      embed = discord.Embed(title="Error", description=f":x: couldnt find the Muted role pls set a Mute role using {prefi}mute_role", color=color())
      await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member = None):
  Mute_rol = (discord.utils.get(user.guild.roles, name=f"{Mute_roles[str(ctx.guild.id)]}"))
  if data["unmute_settings"]["unmute"] == True:
    if user != None:
      if ctx.author.top_role > user.top_role and ctx.guild.me.top_role > user.top_role:
        try:
            await user.remove_roles(Mute_rol)
            await ctx.send(f"""{data["unmute_settings"]["text"].replace("[admin]",f"{ctx.author.name}#{ctx.author.discriminator}").replace("[member]",f"{user.name}#{user.discriminator}")}""")
        except:
            await ctx.send(f'pls check if you have made the role Muted')
      elif ctx.author.top_role <= user.top_role:
        await ctx.send("your role is not hght enough")
      elif ctx.guild.me.top_role <= user.top_role:
        await ctx.send("my role is not high enough")
      else:
        await ctx.send("sorry there was an error while executing the command")
    else:
      embed = discord.Embed(title="Unmute", description=f"`{prefi}unmute <user>`", color=color())
      await ctx.send(embed=embed)

@client.command()
async def insult(ctx , user:discord.Member = None):
  #reminder user.id is a integer not a string
  if user == None:
    #note dont forget to user await ctx.send(embed =embed) if u are making an embed
    embed = discord.Embed(title="Insult", description=f"`{prefi}insult <user>`", color=color())
    await ctx.send(embed = embed)
  elif user.id == 755247492601348227:
    await ctx.send('goto hell I am not inulting him')
  else:
    await ctx.send(f'{user.mention} {random.choice(data["insult"])}' )

@client.command()
async def who_is(ctx , user:discord.Member = None):
  if data["who_is"] == True:
    if user == None:
      embed = discord.Embed(title="Who is", description=f"`{prefi}who_is <user>`", color=color())
      await ctx.send(embed=embed)
    else:
      said = ('is','is the','is one of the')
      if str(user.id) in dictionary.keys():
        await ctx.send(f'{user.name}#{user.discriminator} {random.choice(said)} {dictionary[str(user.id)]}')
      elif user.id == 811245830027477013:
        await ctx.send(f'{user.mention} is one of   the greatest admin I have met')
      elif user.id == 755247492601348227:
        await ctx.send(f'{user.name}#{user.discriminator} is my master')

@client.command()
#note never keep any command name that matches with the module you are using
async def rand(ctx , num = None):
  if data["randomn"] == True:
    try:
      if num == None:
        embed = discord.Embed(title="random", description=f"`{prefi}random <max number>`", color=color())
        await ctx.send(embed=embed)
      else:
          num = int(num)
          await ctx.send(f'I choose {random.randint(1,num)}')
    except:
      await ctx.send('sorry I am having some problem pls check if you entered a number')

@client.command()
async def who_is_set(ctx,*,what_to_say = None):
  if data["who_is"] == True:
    if what_to_say == None:
      embed = discord.Embed(title="Who is set", description=f"`{prefi}who_is_set <your apithet>`", color=color())
      await ctx.send(embed=embed)
    else:
      if str(ctx.author.id) in dictionary.keys():
          del dictionary[str(ctx.author.id)]
          dictionary[str(ctx.author.id)] = what_to_say
          with open("who_is.json","w") as who_s:
              json.dump(dictionary,who_s,indent = 4)
      else:
          dictionary[str(ctx.author.id)] = what_to_say
          with open("who_is.json","w") as who_s:
              json.dump(dictionary,who_s,indent = 4)
      await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator} your who_is statement has been added')

#this * is kept so that the program knows to take every word behind it
@client.command(aliases=['wiki', 'wikipedia'])
async def _what(ctx, *, question = None):
  if data["wikipedia"] == True:
    if question == None:
      embed = discord.Embed(title="Wikipedia", description=f"`{prefi}wiki/wikipedia <your question>`", color=color())
      await ctx.send(embed =embed)
    else:
      try:
        await ctx.send(f'{wikipedia.summary(question, sentences=3)}')
      except:
        await ctx.send('you will need to be more specific')

@client.command(aliases = ['search','google'])
async def _google(ctx,*,query = None):
  if data["google_search"] == True:
    if query == None:
      embed = discord.Embed(title="Google", description=f"`{prefi}google/search <your question>`", color=color())
      await ctx.send(embed =embed)
    else:
      if query.lower() in gogle.keys():
        await ctx.send(f"your answer is in {gogle[query]} check it out")
      else:
        for ans in search(query , tld="co.in",num = 1 , stop = 1 , pause = 2):
          await ctx.send(f"your answer is in {ans} check it out")
          gogle[query.lower()] = f"{ans}"
          with open("google.json","w") as g:
            json.dump(gogle , g , indent = 4)

@client.command()
async def mute_role(ctx,role:discord.Role = None):
  if data["mute_settings"]["mute"] == True:
    if role == None:
      embed = discord.Embed(title="Set Mute Role", description=f"`{prefi}mute_role <role>`", color=color())
      await ctx.send(embed =embed)
    else:
      if str(ctx.guild.id) in Mute_roles.keys():
          del Mute_roles[str(ctx.guild.id)]
          Mute_roles[str(ctx.guild.id)] =f"{role}"
          with open("mute_role.json","w") as mr:
              json.dump(Mute_roles , mr , indent = 4)
      else:
          Mute_roles[str(ctx.guild.id)] =f"{role}"
          with open("mute_role.json","w") as mr:
              json.dump(Mute_roles , mr , indent = 4)
      await ctx.send(f"{role} has been set as the Mute role for this server")

#keep_alive()
#client.run(os.getenv("TOKEN"))
client.run(data["TOKEN"])
