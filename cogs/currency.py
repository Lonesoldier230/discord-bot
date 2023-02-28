import disnake
import json
import random
import asyncio
from disnake.ext import commands

with open("./storage/balance.json", "r") as bal:
    bal = json.load(bal)
with open("./storage/work.json","r") as work:
    work = json.load(work)

def color():
    # this program choose colors for the embed randomly
    color = (0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f,
             0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5)
    randclr = random.choice(color)
    return randclr

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
            salary = work[str(ctx.author.id)]["salary"]
            bal[str(ctx.author.id)]["cash"] = bal[str(ctx.author.id)]["cash"]+salary
            
            with open("./storage/balance.json","w") as wrk:
                json.dump(bal,wrk,indent = 4)
                
            embed = disnake.Embed(title = "Work",color = color(),description = f"you earned {salary:,}")
            await ctx.response.send_message(embed = embed)
        else:
            embed = disnake.Embed(title = "Work",color = color(),description=":x: you dont have a job currently")
            
def setup(client):
    client.add_cog(currency(client))