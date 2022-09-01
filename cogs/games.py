import disnake
from disnake.ext import commands
import json
import random

def color():
    # this program choose colors for the embed randomly
    color = (0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f,
             0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5)
    randclr = random.choice(color)
    return randclr

with open('./storage/main.json', 'r') as js:
    data = json.load(js)

class games(commands.Cog):
    
    def __init__(self,client):
        self.client = client
    
    @commands.slash_command(description="Know your Future")
    async def eightball(ctx:disnake.ApplicationCommandInteraction,question:str):
        if data["8ball"] == True:
            responses = ['It is certain.',
                         'It is decidedly so.', 'As I see it, yes.', 'Most likely.', 'Reply hazy, try again.', 'Ask again later.', 'Don\'t count on it.',
                         'My reply is no.', 'Without a doubt.', 'Yes definitely.', 'Outlook good.', 'Yes.', 'Better not tell you now.', 'Cannot predict now.', 'My sources say no.', 'Outlook not so good.'
                         'You may rely on it.', 'Signs point to yes.', 'Concentrate and ask again.', 'Very doubtful.']
            embed = disnake.Embed(title="Answer", color=color(), description=random.choice(responses))
            await ctx.send(embed=embed)
        
        
def setup(client):
    client.add_cog(games(client))