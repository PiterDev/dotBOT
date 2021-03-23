import discord
import random
import asyncio

from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] Module ready: Moderation")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="None"):
        await member.kick(reason=reason)
        kick=discord.Embed(title='User banned:', description=member.mention, color=discord.Color.red())
        kick.add_field(name="Reason:", value=reason)
        await ctx.send(embed=kick)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed=discord.Embed(title='User banned:', description=member.mention, color=discord.Color.red())
        embed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                unban=discord.Embed(title='User ubanned:', description=member.mention, color=discord.Color.green())
                ctx.send(embed=unban)
                await ctx.send(embed=unban)

    @commands.command(aliases=["clean", "broom"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        amount += 1  # Deletes the command from the channel
        if amount == 0:
            await ctx.send("I deleted 0 messages. How useful!")
            asyncio.sleep(0.5)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.channel.purge(limit=amount)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            ban_error=discord.Embed(title='Error:', description='Could not ban user. Rank is too high.', color=discord.Color.gold())
            await ctx.send(embed=ban_error)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            clear_error=discord.Embed(title='Error:', description='Amount of messages must be a number.', color=discord.Color.gold())
            ctx.send(embed=clear_error)      

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            kick_error=discord.Embed(title='Error:', description='Could not kick user. Rank is too high.', color=discord.Color.gold())
            
            await ctx.send(embed=kick_error)

def setup(client):
    client.add_cog(Moderation(client))
