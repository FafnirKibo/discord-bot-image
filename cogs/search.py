import os

import discord
from discord.ext import commands

from main import destFolder, separator, showPagination, pagination


def setup(client):
    client.add_cog(Search(client))


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="search")
    async def search_command(self, ctx, *, animeName):
        nbFolder = 0
        nbScreen = 0
        result = ""
        embeds = []
        # On compte le nombre de dossiers et de screens
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder) and (animeName.lower() in folderName.lower()):
                nbFolder += 1
                nbScreen += len([name for name in os.listdir(destFolder + folderName)])
        i = 0
        nbFol = 0
        page = 0
        nbPage = nbFolder // pagination + (nbFolder % pagination > 0)
        # On récupère tout les noms
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder) and (animeName.lower() in folderName.lower()):
                i += 1
                nbFol += 1
                result = result + "-    " + folderName + " (" + str(
                    len([name for name in os.listdir(destFolder + folderName)])) + ")\n"
                if i % pagination == 0 or nbFol == nbFolder:
                    page += 1
                    embed = discord.Embed(
                        title="Tout les résultats (" + str(nbFolder) + " dossiers pour " + str(nbScreen) + " screens)",
                        description=result, color=discord.Color.blue())
                    embed.add_field(name="Page", value="Page " + str(page) + "/" + str(nbPage))
                    embeds.append(embed)
                    i = 0
                    result = ""
        if not embeds:
            embed = discord.Embed(
                title="Aucun résultat trouvé", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            if len(embeds) == 1:
                await ctx.send(embed=embeds[0])
            else:
                await showPagination(ctx, embeds)

    @commands.command(name="searchAll")
    async def search_all_command(self, ctx):
        nbFolder = 0
        nbScreen = 0
        result = ""
        embeds = []
        # On compte le nombre de dossiers et de screens
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder):
                nbFolder += 1
                nbScreen += len([name for name in os.listdir(destFolder + folderName)])
        i = 0
        nbFol = 0
        page = 0
        nbPage = nbFolder // pagination + (nbFolder % pagination > 0)
        # On récupère tout les noms
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder):
                i += 1
                nbFol += 1
                result = result + "-    " + folderName + " (" + str(
                    len([name for name in os.listdir(destFolder + folderName)])) + ")\n"
                if i % pagination == 0 or nbFol == nbFolder:
                    page += 1
                    embed = discord.Embed(
                        title="Tout les résultats (" + str(nbFolder) + " dossiers pour " + str(nbScreen) + " screens)",
                        description=result, color=discord.Color.blue())
                    embed.add_field(name="Page", value="Page " + str(page) + "/" + str(nbPage))
                    embeds.append(embed)
                    i = 0
                    result = ""
        if not embeds:
            embed = discord.Embed(
                title="Aucun résultat trouvé", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            if len(embeds) == 1:
                await ctx.send(embed=embeds[0])
            else:
                await showPagination(ctx, embeds)

    @commands.command(name="count")
    async def count_command(self, ctx, *, animeName):
        destination = destFolder + animeName + separator
        count = 0
        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            count = len([name for name in os.listdir(destination)])
        embed = discord.Embed(title="Nombre de screen pour " + animeName, description=count, color=discord.Color.blue())
        await ctx.send(embed=embed)
