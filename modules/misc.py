import discord
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("[INFO] Module ready: Misc")

    

    @commands.command()
    async def ping(self, ctx):
        
        embed=discord.Embed(title="Pong!", description=f"Latency: {int(round(self.client.latency, 2) * 1000)}ms", color=0x6af6ec)
        await ctx.send(embed=embed)
    @commands.command()
    async def amogus(self, ctx):
        await ctx.send('Amogus.')
        await ctx.send(file=discord.File(r'Amogus.mp3'))



def setup(client):
    client.add_cog(Misc(client))
