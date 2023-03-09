import disnake
from disnake.ext import commands
import random
from modules.general import color
from modules.general import file_open

data = file_open('./storage/main.json')

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