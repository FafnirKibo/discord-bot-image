import os

import discord
from discord.ext import commands

import variable

client = commands.Bot(command_prefix='.')
token = variable.token
idBoss = variable.idBoss
destFolder = variable.winDest
separator = "\\"
dropboxToken = variable.dropboxToken


@client.event
async def on_ready():
    print("Bot is ready")
    print(token)


async def sendEmbed(ctx, title, description):
    print(description)
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    await ctx.send(embed=embed)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
