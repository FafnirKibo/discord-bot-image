import os

import discord
from discord.ext import commands

from main import destFolder, separator


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
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder) and (animeName.lower() in folderName.lower()):
                nbFolder += 1
                nbScreen += len([name for name in os.listdir(destFolder + folderName)])
                result = result + "-    " + folderName + " (" + str(
                    len([name for name in os.listdir(destFolder + folderName)])) + ")\n"
        if result == "":
            result = "Aucun résultat trouvé"
        embed = discord.Embed(
            title="Tout les résultats (" + str(nbFolder) + " dossiers pour " + str(nbScreen) + " screens)",
            description=result, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name="searchAll")
    async def search_all_command(self, ctx):
        nbFolder = 0
        nbScreen = 0
        result = ""
        for folderName in os.listdir(destFolder):
            folder = os.path.join(destFolder, folderName)
            if os.path.isdir(folder):
                nbFolder += 1
                nbScreen += len([name for name in os.listdir(destFolder + folderName)])
                result = result + "-    " + folderName + " (" + str(
                    len([name for name in os.listdir(destFolder + folderName)])) + ")\n"
        if result == "":
            result = "Aucun résultat trouvé"
        embed = discord.Embed(
            title="Tout les résultats (" + str(nbFolder) + " dossiers pour " + str(nbScreen) + " screens)",
            description=result, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name="count")
    async def count_command(self, ctx, *, animeName):
        destination = destFolder + animeName + separator
        count = 0
        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            count = len([name for name in os.listdir(destination)])
        embed = discord.Embed(title="Nombre de screen pour " + animeName, description=count, color=discord.Color.blue())
        await ctx.send(embed=embed)
