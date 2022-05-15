import os
import zipfile
from random import randint

import discord
import dropbox
from discord.ext import commands

from main import destFolder, separator, sendEmbed
from variable import dropboxToken


def setup(client):
    client.add_cog(Send(client))


class Send(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="send")
    async def send(self, ctx, userID, nbImage, *, animeName):
        titre = "Envoie d'un screen de " + animeName
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3
        user = self.client.get_user(userID) or await self.client.fetch_user(userID)

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            if os.path.exists(destination + imageName):
                # Envoie de l'image
                await user.send(animeName + " " + nbImage + " :")
                await user.send(file=discord.File(destination + imageName))
                await sendEmbed(ctx, "Screen '" + imageName + "' bien envoyé à " + user.name, "")
            else:
                await sendEmbed(ctx, titre, "Il n'existe pas de screen " + nbImage + " pour " + animeName)
        else:
            await sendEmbed(ctx, titre, "Aucun screen existe pour " + animeName)

    @commands.command(name="sendFrom")
    async def sendFrom(self, ctx, userID, nbImage, *, animeName):
        titre = "Envoie des screens de " + animeName + " à partir du " + nbImage
        await sendEmbed(ctx, titre, "Début de l'envoie")
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3
        user = self.client.get_user(userID) or await self.client.fetch_user(userID)

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            if os.path.exists(destination + imageName):
                # Création du ZIP
                archiveName = animeName + "_" + user.name + ".zip"
                zipObj = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
                # Envoie de l'image
                await user.send(animeName + " depuis l'image " + nbImage + " :")
                await user.send(file=discord.File(destination + imageName))
                zipObj.write(destination + imageName, arcname=imageName)
                await sendEmbed(ctx, "Screen '" + imageName + "' bien envoyé à " + user.name, "")
                # On continue à envoyer si il en reste
                count = int(nbImage) + 1
                imageName = animeName + " - " + str(count).zfill(digits) + ".png"
                while os.path.exists(destination + imageName):
                    await user.send(file=discord.File(destination + imageName))
                    # Ajout de l'image à l'archive
                    zipObj.write(destination + imageName, arcname=imageName)
                    await sendEmbed(ctx, "Screen '" + imageName + "' bien envoyé à " + user.name, "")
                    count += 1
                    imageName = animeName + " - " + str(count).zfill(digits) + ".png"
                zipObj.close()
                await sendEmbed(ctx, titre, "Fin de l'envoie")
                await self.saveDropbox(ctx, archiveName, user)
            else:
                await sendEmbed(ctx, titre, "Il n'existe pas de screen " + nbImage + " pour " + animeName)
        else:
            await sendEmbed(ctx, titre, "Aucun screen existe pour " + animeName)

    @commands.command(name="sendFromTo")
    async def sendFromTo(self, ctx, userID, nbImageFrom, nbImageTo, *, animeName):
        titre = "Envoie des screens de " + animeName + " du " + nbImageFrom + " au " + nbImageTo
        await sendEmbed(ctx, titre, "Début de l'envoie")
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3
        user = self.client.get_user(userID) or await self.client.fetch_user(userID)

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération de l'image
            imageName = animeName + " - " + str(nbImageFrom).zfill(digits) + ".png"
            if os.path.exists(destination + imageName):
                # Création du ZIP
                archiveName = animeName + "_" + user.name + ".zip"
                zipObj = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
                # Envoie de l'image
                await user.send(
                    animeName + " depuis le screen " + nbImageFrom + " au screen " + nbImageTo + " (si il existe) :")
                await user.send(file=discord.File(destination + imageName))
                zipObj.write(destination + imageName, arcname=imageName)
                await sendEmbed(ctx, "Screen '" + imageName + "' bien envoyé à " + user.name, "")
                # On continue à envoyer si il en reste
                count = int(nbImageFrom) + 1
                imageName = animeName + " - " + str(count).zfill(digits) + ".png"
                while os.path.exists(destination + imageName) and count <= int(nbImageTo):
                    await user.send(file=discord.File(destination + imageName))
                    # Ajout de l'image à l'archive
                    zipObj.write(destination + imageName, arcname=imageName)
                    await sendEmbed(ctx, "Screen '" + imageName + "' bien envoyé à " + user.name, "")
                    count += 1
                    imageName = animeName + " - " + str(count).zfill(digits) + ".png"
                zipObj.close()
                await sendEmbed(ctx, titre, "Fin de l'envoie")
                await self.saveDropbox(ctx, archiveName, user)
            else:
                await sendEmbed(ctx, titre, "Il n'existe pas de screen " + nbImageFrom + " pour " + animeName)
        else:
            await sendEmbed(ctx, titre, "Aucun screen existe pour " + animeName)

    async def saveDropbox(self, ctx, file, user):
        dbx = dropbox.Dropbox(oauth2_access_token=dropboxToken)
        n = randint(0, 10000)
        archiveName = str(n) + '-' + file
        with open(file, 'rb') as f:
            dbx.files_upload(f.read(), '/' + archiveName)
        link = dbx.sharing_create_shared_link_with_settings('/' + archiveName)
        await user.send("Archive des screens : " + str(link.url))
        await sendEmbed(ctx, "Archive '" + archiveName + "' bien envoyée à " + user.name, "")
        os.remove(file)
