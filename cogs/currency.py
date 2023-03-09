import disnake
import json
import time
from disnake.ext import commands
from modules.general import color
from modules.general import file_open
from modules.shop import embeder

bal = file_open("./storage/balance.json")
work = file_open("./storage/work.json")

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
            
    @commands.slash_command(description= "to look for products to buy")
    async def shop(ctx:disnake.ApplicationCommandInteraction):
        embed = embeder(ctx)
        nam = "all"
        shop_items = file_open("./storage/shop_items.json")
        number = 0
        
        async def callback_select(interactions):
            nam = select_menu.values[0]            
            embed = embeder(ctx,nam)
            number = 0  
            await interactions.response.edit_message(embed = embed,view = view)
            
        async def callback_button1(interactions):
            number += 1
            embed = embeder(ctx,number = number)
            await interactions.response.edit_message(embed=embed, view=view)
            button2.disabled = False
            if len(list(shop_items[nam].keys())) < 10+10*number:
                button1.disabled = True
            
            
        async def callback_button2(interactions):
            number -= 1
            embed = embeder(ctx, number=number)
            button1.disabled = False
            if len(list(shop_items[nam].keys())) < 10+10*number:
                button2.disabled = True
            await interactions.response.edit_message(embed=embed, view=view)
        
        options = []
        for n in shop_items.keys():
            options.append(disnake.SelectOption(label=n))
        select_menu = disnake.ui.Select(options=options,placeholder="Results")
        button1 = disnake.ui.Button(label="<", style=disnake.ButtonStyle.primary)
        button2 = disnake.ui.Button(label=">", style=disnake.ButtonStyle.primary)
        
        select_menu.callback = callback_select
        button1.callback = callback_button1
        button1.disabled = True
        button2.callback = callback_button2
        
        view = disnake.ui.View()
        view.add_item(select_menu)
        view.add_item(button1)
        view.add_item(button2)
        
        await ctx.send(embed=embed, view=view)
        
def setup(client):
    client.add_cog(currency(client))