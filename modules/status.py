import discord
from discord.ext import commands



class Status(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('[INFO] Module ready: Status')
        await self.client.change_presence(activity=discord.Streaming(name='Powerpoint', url='https://www.youtube.com/channel/UCZQ8GSJlEOuMSvs1IdP2xLg'))


def setup(client):
    client.add_cog(Status(client))
