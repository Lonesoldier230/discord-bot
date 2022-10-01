import disnake
from disnake.ext import commands  
import requests
import json

def search(type,name):
    if type == "anime":
        url = "https://api.jikan.moe/v4/anime"
    elif type == "manga":
        url = "https://api.jikan.moe/v4/manga"
    querystring = {"q": name, "limit": 10}
    response = requests.get(url=url, params=querystring)
    if response.status_code == 200:
        a = []
        top_search = {}
        r = json.loads(response.text)
        for n in r["data"]:
            for i in n["genres"]:
                a.append(i["name"])
            title = n["title"]
            top_search[title] = {}
            top_search[title]["genre"] = ",".join(shortner(".".join(a)))
            top_search[title]["id"] = n["mal_id"]
            top_search[title]["url"] = n["url"]
            top_search[title]["synopsis"] = n["synopsis"]
            top_search[title]["image"]=n["images"]["jpg"]["image_url"]
        return top_search
    else:
        return "Error"
    
def shortner(paragraph):
    a = paragraph.split('.')
    if len(a) > 5:
        return a[0:5]
    else:
        return a

class Anime(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.slash_command()
    async def manga_search(ctx:disnake.ApplicationCommandInteraction,name):
        options = []
        result = search("manga", name)
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options,placeholder="Results")
        manga_id = result[a]["id"]
        url = result[a]["url"]
        synopsis = ".".join(shortner(result[a]["synopsis"]))
        
        embed = disnake.Embed(title=a, url= url, color=0xFF5733)
        embed.set_thumbnail(url = result[a]["image"])
        embed.add_field(name = "Genre", value = result[a]["genre"])
        embed.add_field(name="Synopsis", value=synopsis, inline=False)
        embed.set_footer(text = f"#{manga_id}")
        
        async def calback(interaction):
            nam = select_menu.values[0]
            manga_id = result[nam]["id"]
            result1 = requests.get(
                f"https://api.jikan.moe/v4/manga/{manga_id}/full")
            result1 = json.loads(result1.text)
            url = result[nam]["url"]
            synopsis = ".".join(shortner(result[nam]["synopsis"]))
            
            embed = disnake.Embed(title=nam, url=url, color=0xFF5733)
            embed.set_thumbnail(url=result[nam]["image"])
            embed.add_field(name="Genre", value=result[nam]["genre"])
            embed.add_field(name="Synopsis", value=synopsis, inline=False)
            embed.set_footer(text = f"#{manga_id}")
            await interaction.response.edit_message(embed=embed, view=view)
            
        select_menu.callback= calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed = embed,view=view)
        
    @commands.slash_command()
    async def anime_search(ctx: disnake.ApplicationCommandInteraction, name):
        options = []
        result = search("anime", name)
        for n in result.keys():
            options.append(disnake.SelectOption(label=n))
        a = list(result.keys())[0]
        select_menu = disnake.ui.Select(options=options, placeholder="Results")
        anime_id = result[a]["id"]
        url = result[a]["url"]
        synopsis = ".".join(shortner(result[a]["synopsis"]))
        
        embed = disnake.Embed(
            title=a, url=url, color=0xFF5733)
        embed.set_thumbnail(url=result[a]["image"])
        embed.add_field(name="Genre", value=result[a]["genre"],inline=False)
        embed.add_field(name="Synopsis",value = synopsis,inline=False)
        embed.set_footer(text=f"#{anime_id}")

        async def calback(interaction):
            nam = select_menu.values[0]
            anime_id = result[nam]["id"]
            url = result[nam]["url"]
            synopsis = ".".join(shortner(result[nam]["synopsis"]))        
            embed = disnake.Embed(title=nam, url=url, color=0xFF5733)
            embed.set_thumbnail(
                url=result[nam]["image"])
            embed.add_field(name="Genre", value=result[nam]["genre"])
            embed.add_field(name="Synopsis", value=synopsis, inline=False)
            embed.set_footer(text=f"#{anime_id}")
            await interaction.response.edit_message(embed=embed, view=view)
            
        select_menu.callback = calback
        view = disnake.ui.View()
        view.add_item(select_menu)
        await ctx.send(embed=embed, view=view)
            

def setup(client):
  client.add_cog(Anime(client))
