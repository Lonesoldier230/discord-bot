import disnake
from disnake.ext import commands  
import requests
import random
import json


def color():
    # this program choose colors for the embed randomly
    color = (0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f,
             0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5)
    randclr = random.choice(color)
    return randclr

def search(type,name=None):
    if type == "anime":
        querystring = {"q": name, "limit": 10}
        url = "https://api.jikan.moe/v4/anime"
        response = requests.get(url=url, params=querystring)
    elif type == "manga":
        querystring = {"q": name, "limit": 10}
        url = "https://api.jikan.moe/v4/manga"
        response = requests.get(url=url, params=querystring)
    elif type == "topanime":
        url = "https://api.jikan.moe/v4/top/anime"
        response = requests.get(url= url)
    elif type == "topmanga":
        url = "https://api.jikan.moe/v4/top/manga"
        response = requests.get(url = url)
    if response.status_code == 200:
        a = []
        top_search = {}
        r = json.loads(response.text)
        for n in r["data"]:
            for i in n["genres"]:
                if i not in a:
                    a.append(i["name"])
            title = n["title"]
            top_search[title] = {}
            if a != None:
                top_search[title]["genre"] = ",".join(shortner(".".join(a)))
            else:
                top_search[title]["genre"] = None 
            top_search[title]["id"] = n["mal_id"]
            top_search[title]["url"] = n["url"]
            top_search[title]["synopsis"] = n["synopsis"]
            top_search[title]["image"]=n["images"]["jpg"]["image_url"]
            top_search[title]["rank"] = n["rank"]
            if type == "anime" or type == "topanime":
                top_search[title]["episodes"] = n["episodes"]
            top_search[title]["score"] = n["score"]
        return top_search
    else:
        raise ValueError
    
def shortner(paragraph):
    if paragraph == None:
        return None
    else: 
        a = paragraph.split('.')
        if len(a) > 5:
            return a[0:5]
        else:
            return a

def embeder(result,name,type=None):
    id = result[name]["id"]
    url = result[name]["url"]
    if result[name]["synopsis"] != None:
        synopsis = ".".join(shortner(result[name]["synopsis"]))
    else:
        synopsis = None
    embed = disnake.Embed(title=name, url=url, color=color())
    embed.set_thumbnail(url=result[name]["image"])
    embed.add_field(name=":regional_indicator_g: Genre",value=result[name]["genre"], inline=False)
    embed.add_field(name=":100: Score", value=result[name]["score"], inline=True)
    embed.add_field(name=":trophy: Rank",value=result[name]["rank"], inline=True)
    if type == "anime":
        embed.add_field(name=":play_pause: Episodes",value=result[name]["episodes"], inline=True)
    embed.add_field(name=":scroll: Synopsis",value=synopsis, inline=False)
    embed.set_footer(text=f"#{id}")
    return embed

class Anime(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.slash_command(description="Search any Manga you like")
    async def manga_search(ctx:disnake.ApplicationCommandInteraction,name):
        options = []
        result = search("manga", name)
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options,placeholder="Results")
        embed = embeder(result, a)
        
        async def calback(interaction):
            nam = select_menu.values[0]
            embed = embeder(result,nam)
            await interaction.response.edit_message(embed=embed, view=view)
            
        select_menu.callback= calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed = embed,view=view)
        
    @commands.slash_command(description="Search any Anime you like")
    async def anime_search(ctx: disnake.ApplicationCommandInteraction, name):
        options = []
        result = search("anime", name)
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options, placeholder="Results")
        embed = embeder(result, a,"anime")

        async def calback(interaction):
            nam = select_menu.values[0]
            embed = embeder(result, nam,"anime")
            await interaction.response.edit_message(embed=embed, view=view)
            
        select_menu.callback = calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed=embed, view=view)
        
    @commands.slash_command(description="Search the top Anime")
    async def top_anime(ctx: disnake.ApplicationCommandInteraction):
        options = []
        result = search("topanime")
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options, placeholder="Results")
        embed = embeder(result, a, "anime")

        async def calback(interaction):
            nam = select_menu.values[0]
            embed = embeder(result, nam, "anime")
            await interaction.response.edit_message(embed=embed, view=view)

        select_menu.callback = calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed=embed, view=view)
        
    @commands.slash_command(description="Search the top Manga")
    async def top_manga(ctx: disnake.ApplicationCommandInteraction):
        options = []
        result = search("topmanga")
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options, placeholder="Results")
        embed = embeder(result, a)

        async def calback(interaction):
            nam = select_menu.values[0]
            embed = embeder(result, nam)
            await interaction.response.edit_message(embed=embed, view=view)

        select_menu.callback = calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed=embed, view=view)
            

def setup(client):
  client.add_cog(Anime(client))