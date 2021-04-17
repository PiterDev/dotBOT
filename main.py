import time
import discord
import os
from discord.ext import commands
from keep_alive import keep_alive
from replit import db


keys = db.keys()
for key in keys:
    print(f'{key}:{db[key]}')


intents = discord.Intents.default()
intents.members = True


print("Loading bot...")


client = commands.Bot(command_prefix=".", intents=intents)

@client.event
async def on_ready():
    print("=============================")
    print(f'[INFO] Bot invite: https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot')

@client.command()
async def load(ctx, extension):
    if str(ctx.author) == "Piter#1234":
        client.load_extension(f'modules.{extension}')
    else:
        await ctx.send("Nope")


@client.command()
async def reload(ctx, extension):
    if str(ctx.author) == "Piter#1234":
        client.unload_extension(f'modules.{extension}')
        client.load_extension(f'modules.{extension}')
    else:
        await ctx.send("Nope")


@client.command()
async def unload(ctx, extension):
    if str(ctx.author) == "Piter#1234":
        client.unload_extension(f'modules.{extension}')
    else:
        await ctx.send("Nope")


@client.event
async def on_command_error(ctx, error,):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, discord.Forbidden):
        ctx.send("Looks like I don't have permissions. This bot requires administrator permissions to work.")
    msg = ctx.message.content
    (ctx.message.id)
    print(f'[WARN] Error encountered: ({error}) message: {msg}')

print("Loading modules...")
time.sleep(1)
for filename in os.listdir('modules'):
    if filename.endswith('.py'):
        client.load_extension(f'modules.{filename[:-3]}')

keep_alive()
client.run(os.environ['TOKEN'])