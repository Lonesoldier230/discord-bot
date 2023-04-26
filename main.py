# made by Lone_soldier230
# import
import random
from disnake.ext import commands, tasks
import disnake
import os
import requests
import json
from json.decoder import JSONDecodeError
import time
from modules.general import color
from modules.general import file_open
#from dotenv import load_dotenv
# load_dotenv()
#from keep_alive import keep_alive


# def
intents = disnake.Intents.all()


backup_data = {"TOKEN": None, "8ball": True, "Custom_commands": {"hello": "hi how are you"}, "kick_settings": {"kick": True, "text": "[admin] kicked [member]"}, "ban_settings": {"ban": True, "text": "[admin] banned [member]"}, "unban_settings": {"unban": True, "text": "[admin] unbanned [member]"}, "role_settings": {
    "role": True, "text": "[admin] has roled [member]"}, "unrole_settings": {"unrole": True, "text": "[admin] has unroled [member]"}, "mute_settings": {"mute": True, "text": "[member] has been muted by [admin]"}, "unmute_settings": {"unmute": True, "text": "[member] has been unmuted by [admin]"}, "banned_words": [""], "banned_sites": [""]}

# most essential program it finds where this file is located and changes dir here
path1 = __file__.replace('main.py', '')
paths = os.path.join(path1)
os.chdir(paths)


# this is where file is handeled
# config
for i in range(3):
    configurater = {0: "you made an error in main.json you have 60 seconds",
                    1: "can you check main.json again you have 60 seconds"}
    try:
        data = file_open('./storage/main.json')
    except JSONDecodeError as e:
        if i < 2:
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
    with open('./storage/main.json', 'w') as hson:
        json.dump(backup_data, hson, indent=4)
        data = dict(backup_data)

if data["TOKEN"] == None:
    print('pls enter your TOKEN')
    exit()

try:
    Mute_roles = file_open("./storage/mute_role.json")
except:
    print("hey dont mess with mute_role.json")


# this is the brain of the bot
client = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned )
prefi = "/"
# body

#!improve help command
@client.remove_command('help')
@client.slash_command(description="List of all the commands")
async def help(ctx: disnake.ApplicationCommandInteraction):
    colour = color()
    embed = disnake.Embed(title="Help", color=colour)
    embed.add_field(
        name="Moderator", value=f"`{prefi}help moderator/mod/commands`", inline=False)
    embed.add_field(
        name="Search", value=f"`{prefi}help search/look/google`", inline=False)
    embed.add_field(name="Fun", value=f"`{prefi}help fun`", inline=False)
    cate = disnake.ui.Select(options=[
        disnake.SelectOption(label="moderator"),
        disnake.SelectOption(label="fun")])
    async def my_callback(interaction):
        embed = disnake.Embed(title="Help", color=color())
        if cate.values[0] == "moderator":
            embed.add_field(
                name="Kick", value=f"{prefi}kick `user:` `reason:`", inline=False)
            embed.add_field(
                name="Ban", value=f"{prefi}ban `user:` `reason:`", inline=False)
            embed.add_field(
                name="Mute", value=f"{prefi}mute `user:`", inline=False)
            embed.add_field(
                name="Unmute", value=f"{prefi}unmute `user:`", inline=False)
            embed.add_field(
                name="Role", value=f"{prefi}role `user:` `role:`", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)
        elif cate.values[0] == "fun":
            embed.add_field(
                name='Insult', value=f"`{prefi}insult <member>`", inline=False)
            embed.add_field(
                name='Random', value=f"`{prefi}rand <max number>`", inline=False)
            embed.add_field(name='Who is set',
                            value=f"`{prefi}who_is_set <your apithet>`", inline=False)
            embed.add_field(
                name='Who is', value=f"`{prefi}whois <user>`", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)
    cate.callback = my_callback
    view = disnake.ui.View()
    view.add_item(cate)
    await ctx.send(embed=embed, view=view)


# this loads the config file
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
    # to change activity and status of the bot
    await client.change_presence(status=disnake.Status.online, activity=disnake.Game(f'{prefi}help'))
    print('I am ready')


@client.event
async def on_member_join(member: disnake.Member):
    print(f'{member.name} has joined')


@client.event
async def on_member_leave(member: disnake.Member):
    print(f'{member.name} left the server')


@client.event
async def on_connect():
    print('connected to server')


@client.slash_command(description = "Check if servers are online or the latency of the bot")
async def ping(ctx:disnake.ApplicationCommandInteraction, url:str=None):
    timeout = 1
    if url != None:
        try:
            request = requests.get(url, timeout=timeout)
            await ctx.send('the server is online')
        except:
            await ctx.send('the server is offline or doesnt exist')
    else:
        await ctx.send(f'pong {round(client.latency*1000)}ms')

# keep_alive()
# client.run(os.getenv("TOKEN"))
if __name__ == "__main__":
    client.run(data["TOKEN"])