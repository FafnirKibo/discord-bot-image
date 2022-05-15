import os
from random import randint

import discord
from discord.ext import commands

from main import destFolder, separator


def setup(client):
    client.add_cog(Show(client))


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="show")
    async def show_command(self, ctx, nbImage, *, animeName):
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            url = destination + imageName
            if os.path.exists(url):
                # Envoie du message avec l'image
                file = discord.File(url)
                embed = discord.Embed(title=imageName, color=discord.Color.blue())
                embed.set_image(url="attachment://" + url)
                await ctx.send(file=file, embed=embed)
            else:
                embed = discord.Embed(title="Pas de screen " + nbImage + " pour " + animeName,
                                      color=discord.Color.blue())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Pas de screen pour " + animeName, color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="random")
    async def random(self, ctx, *, animeName):
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # On tire un numéro au hasard parmi les images disponibles
            nbImage = randint(1, len([name for name in os.listdir(destination)]))
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            url = destination + imageName
            # Envoie du message avec l'image
            file = discord.File(url)
            embed = discord.Embed(title=imageName, color=discord.Color.blue())
            embed.set_image(url="attachment://" + url)
            await ctx.send(file=file, embed=embed)

        else:
            embed = discord.Embed(title="Pas de screen pour " + animeName, color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="fullRandom")
    async def full_random_command(self, ctx):
        # On tire un numéro au hasard parmi les anime disponibles
        nbAnime = randint(0, len([name for name in os.listdir(destFolder)]) - 1)
        animeName = os.listdir(destFolder)[nbAnime]
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # On tire un numéro au hasard parmi les images disponibles
            nbImage = randint(1, len([name for name in os.listdir(destination)]))
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            url = destination + imageName
            # Envoie du message avec l'image
            file = discord.File(url)
            embed = discord.Embed(title=imageName, color=discord.Color.blue())
            embed.set_image(url="attachment://" + url)
            await ctx.send(file=file, embed=embed)

        else:
            embed = discord.Embed(title="Pas de screen pour " + animeName, color=discord.Color.blue())
            await ctx.send(embed=embed)
