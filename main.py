import os

import DiscordUtils
import discord
from discord.ext import commands

import variable

client = commands.Bot(command_prefix='.')
token = variable.token
idBoss = variable.idBoss
destFolder = variable.winDest
separator = "\\"
dropboxToken = variable.dropboxToken
pagination = 25


@client.event
async def on_ready():
    print("Bot is ready")
    print(token)


async def sendEmbed(ctx, title, description):
    print(description)
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    await ctx.send(embed=embed)


async def showPagination(ctx, embeds):
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    await paginator.run(embeds)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
