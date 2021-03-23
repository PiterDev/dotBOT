import discord
import json
from discord.ext import commands


class NotTest(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def karma(self, ctx, user : discord.User):

        with open('karma.json', 'r') as f:
                karma = json.load(f)
        user_karma = round(karma[str(user.id)])

        embed1=discord.Embed(title=str(user), description=f'Karma: {user_karma}', color=0x63d544)

        await ctx.send(embed=embed1)


def setup(client):
    client.add_cog(NotTest(client))
