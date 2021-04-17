import discord
from discord.ext import commands


class NotTest(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def toascii(self, ctx):
        print(ctx.message.attachments)

        



def setup(client):
    client.add_cog(NotTest(client))
