import discord
from discord.ext import commands, tasks
from discord.utils import get
import json
import asyncio
import os



class AntiRaid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open('max-server-joins.json', 'r') as f2:
            max_joins = json.load(f2)
        if max_joins[str(member.guild.id)][3]:

            with open('server-joins.json', 'r') as f:
                joins = json.load(f)
            joins[str(member.guild.id)] = str(int(joins[str(member.guild.id)])+1)

            with open('server-joins.json', 'w') as f:
                json.dump(joins, f, indent=4)

            

            if int(joins[str(member.guild.id)]) >= int(max_joins[str(member.guild.id)][0]):

                to_wait = int(joins[str(member.guild.id)]) * 5
                await asyncio.sleep(to_wait)
                role = get(member.guild.roles, name=max_joins[str(member.guild.id)][2])
                try:
                    await member.add_roles(role)
                except discord.errors.Forbidden:
                    owner = member.guild.owner 

                    await owner.send("The bot seems to be malfunctioing due to permissions. Check if the bot has administrator permissions and try to put it higher in the role hierachy")
                in_words = str(to_wait) + " seconds"
                if to_wait > 60:
                    to_wait /= 60
                    in_words = str(to_wait) + " hours"
                    if to_wait > 24:
                        to_wait /= 24
                        in_words = str(to_wait) + " days"
                

                


                embed=discord.Embed(description=f"Hello! The server is currently crowded. You will be given accesto the server in {in_words}. If you do not, please contact the server admins.", color=0x6af0bd)

                await member.send(embed = embed)
            else:
                role = get(member.guild.roles, name='Member')
                await member.add_roles(role)

    async def reset_value(self, time: int, server):

        while True:
            await asyncio.sleep(time)
            with open('server-joins.json', 'r') as f:
                joins = json.load(f)
            with open('max-server-joins.json', 'r') as f2:
                max_joins = json.load(f2)
            if time != int(max_joins[str(server.id)][1]):
                self.client.loop.stop()
            joins[str(server.id)] = "0"
            with open('server-joins.json', 'w') as f:
                json.dump(joins, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('server-joins.json', 'r') as f:
            joins = json.load(f)

        if str(guild.id) not in joins:
            joins[str(guild.id)] = '0'
            with open('server-joins.json', 'w') as f:
                json.dump(joins, f, indent=4)

        with open('max-server-joins.json', 'r') as f2:
            max_joins = json.load(f2)

        if str(guild.id) not in max_joins:
            max_joins[str(guild.id)] = ['0', '60', 'member', False]
            with open('max-server-joins.json', 'w') as f2:
                json.dump(max_joins, f, indent=4)

        self.client.loop.create_task(self.reset_value(int(max_joins[str(guild.id)][1]), guild))

    @commands.Cog.listener()
    async def on_ready(self):
        print("[INFO] Module ready: Anti Raid")
        for guild in self.client.guilds:
            with open('max-server-joins.json', 'r') as f2:
                max_joins = json.load(f2)
            with open('server-joins.json', 'r') as f:
                joins = json.load(f)
            if str(guild.id) not in max_joins:
                max_joins[str(guild.id)] = ['0', '60', 'member', False]
                with open('max-server-joins.json', 'w') as f:
                    json.dump(max_joins, f, indent=4)
            if str(guild.id) not in joins:
                joins[str(guild.id)] = 0
                with open('server-joins.json', 'w') as f:
                    json.dump(joins, f, indent=4)
            if max_joins[str(guild.id)][3]:
                self.client.loop.create_task(self.reset_value(int(max_joins[str(guild.id)][1]), guild))

    @commands.command()
    async def antiraid(self, ctx):
        await ctx.send("Would you like to enable or disable the anti-raid feature?. ON/OFF")
        msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)


        if not msg.content.lower() == 'off' and not msg.content.lower() == 'on':
            await ctx.send('Invalid argument given. Please restart.')
            return
        with open('max-server-joins.json', 'r') as f2:
                max_joins = json.load(f2)

        if msg.content.lower() == 'off':
            await ctx.send('Turning off...')
            
            max_joins[str(ctx.guild.id)] = [max_joins[str(ctx.guild.id)][0], max_joins[str(ctx.guild.id)][1], max_joins[str(ctx.guild.id)][2], False]
            with open('max-server-joins.json', 'w') as f:
                    json.dump(max_joins, f, indent=4)
            await ctx.send('Disabled succesfully!')
        else:
            await ctx.send("Starting setup. Please note that if you do not reply for a minute it will be cancelled.")

            await ctx.send("Alright. First, send the name of the role you would like to be given to new members. (without the '@')")

            msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)



            if get(ctx.guild.roles, name=msg.content):
                role = get(ctx.guild.roles, name=msg.content)
            else:
                await ctx.send('Invalid role given. Please restart setup.')
                return
            await ctx.send("""Alright. Now, please specify a time period in seconds you want to reset the join amount. Minimum is 60 and maximum is 86400. Examples:
            - 60 (one minute)
            - 3600 (one hour)
            - 86400 (one day)""")
            msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)

            if not str(msg.content).isnumeric():
                await ctx.send('Given time is not a number. Please restart setup.')
                return
            elif int(msg.content) > 86400:
                await ctx.send('Invalid time given. Please restart setup.')
                return
            else:
                await ctx.send(f'Time set to {int(msg.content)} seconds.')
                server_time = int(msg.content)

            await ctx.send("How many users can join in the specified time before the antiraid turns on?")

            msg = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
            if not str(msg.content).isnumeric():
                await ctx.send('Given amount is not a number. Please restart setup.')
                return
            else:
                user_joins = str(msg.content)
            await ctx.send('Applying settings...')
            max_joins[str(ctx.guild.id)] = [user_joins, str(server_time), str(role), True]
            with open('max-server-joins.json', 'w') as f:
                    json.dump(max_joins, f, indent=4)
            await ctx.send("Applied succesfully! Deleting messages...")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=13)

        



def setup(client):
    client.add_cog(AntiRaid(client))
