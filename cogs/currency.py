import disnake
import json
import random
import time
import asyncio
from disnake.ext import commands
from modules.general import color

with open("./storage/balance.json", "r") as bal:
    bal = json.load(bal)
with open("./storage/work.json","r") as work:
    work = json.load(work)

class currency(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    @commands.slash_command(description = "check your and others balace")
    async def balance(ctx:disnake.ApplicationCommandInteraction,user:disnake.User = None):
        if user == None:
            if str(ctx.author.id) in bal.keys():
                cash = bal[str(ctx.author.id)]["cash"]
                bank = bal[str(ctx.author.id)]["bank"]
                embed = disnake.Embed(title="Balance",color = color(),description=f"**Cash:**⏣ {cash:,}\n**Bank:**⏣ {bank:,}")
                embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}'s balance")
                await ctx.response.send_message(embed=embed) 
            else:
                embed = disnake.Embed(title="Balance", color=color(), description=f"**Cash:**⏣ 0\n**Bank:**⏣ 0")
                embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}'s balance")
                await ctx.response.send_message(embed=embed)
                bal[f"{ctx.author.id}"] = {"cash":"0","bank":"0"}
                with open("./storage/balance.json","w") as edit:
                    json.dump(bal,edit,indent=4)
        else:
            if str(user.id) in bal.keys():
                cash = bal[str(user.id)]["cash"]
                bank = bal[str(user.id)]["bank"]
                embed = disnake.Embed(title="Balance", color=color(), description=f"**Cash:**⏣ {cash:,}\n**Bank:**⏣ {bank:,}")
                embed.set_footer(text=f"{user.name}#{user.discriminator}'s balance")
                await ctx.response.send_message(embed=embed)
            else:
                embed = disnake.Embed(title="Balance", color=color(), description=f"**Cash:**⏣ 0\n**Bank:**⏣ 0")
                embed.set_footer(text = f"{user.name}#{user.discriminator}'s balance")
                await ctx.response.send_message(embed=embed)
                bal[f"{user.id}"] = {"cash": "0", "bank": "0"}
                with open("./storage/balance.json", "w") as edit:
                    json.dump(bal, edit, indent=4)
#!timer needs to be added

    @commands.slash_command()
    async def work(ctx:disnake.ApplicationCommandInteraction):
        if str(ctx.author.id) in work:
            duration = time.time() - bal[str(ctx.author.id)]["time"]
            if duration > 30.00:
                salary = work[str(ctx.author.id)]["salary"]
                bal[str(ctx.author.id)]["cash"] = bal[str(ctx.author.id)]["cash"]+salary
                bal[str(ctx.author.id)]["time"] = time.time()
                with open("./storage/balance.json","w") as wrk:
                    json.dump(bal,wrk,indent = 4)
                    
                embed = disnake.Embed(title = "Work",color = color(),description = f"you earned {salary:,}")
                await ctx.response.send_message(embed = embed)
            else:
                embed = disnake.Embed(title="Work", color=color(), description=f"please wait for {30 - int(duration)}")
                await ctx.response.send_message(embed=embed)
                
        else:
            embed = disnake.Embed(title = "Work",color = color(),description=":x: you dont have a job currently")
            
def setup(client):
    client.add_cog(currency(client))