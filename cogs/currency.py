import disnake
from disnake.ext import commands

class currency(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
def setup(client):
    client.add_cog(currency(client))