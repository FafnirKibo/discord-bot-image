import os
import shutil

import dropbox
from discord.ext import commands

from main import destFolder, separator, sendEmbed
from variable import idBoss, dropboxToken


def setup(client):
    client.add_cog(Delete(client))


class Delete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="deleteLast")
    async def delete_last_command(self, ctx, *, animeName):
        title = "Suppression du dernier screen de " + animeName
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération du nombre de fichier dans le dossier
            count = len([name for name in os.listdir(destination)])
            imageName = animeName + " - " + str(count).zfill(digits) + ".png"
            if os.path.exists(destination + imageName):
                os.remove(destination + imageName)
                await sendEmbed(ctx, title, "Suppression réussie")
            else:
                await sendEmbed(ctx, title, "Il existe aucun screen pour " + animeName)
        else:
            await sendEmbed(ctx, title, "Il existe aucun screen pour " + animeName)

    @commands.command(name="delete")
    async def delete_command(self, ctx, animeName, nbImage):
        title = "Suppression du screen " + nbImage + " de " + animeName
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3

        # On regarde si une image existe pour l'anime
        if os.path.exists(destination):
            # Récupération du nombre de fichier dans le dossier
            imageName = animeName + " - " + str(nbImage).zfill(digits) + ".png"
            if os.path.exists(destination + imageName):
                # On supprime l'image
                os.remove(destination + imageName)
                await sendEmbed(ctx, title, "Suppression réussie")
                # On renomme toutes les autres d'après si ce n'était pas la dernière
                count = int(nbImage) + 1
                imageName = destination + animeName + " - " + str(count).zfill(digits) + ".png"
                while os.path.exists(imageName):
                    newName = destination + animeName + " - " + str(int(count) - 1).zfill(digits) + ".png"
                    os.rename(imageName, newName)
                    count += 1
                    imageName = destination + animeName + " - " + str(count).zfill(digits) + ".png"
                    await sendEmbed(ctx, "Renommage des screens suivants", "Screen bien renommé : " + newName)
            else:
                await sendEmbed(ctx, title, "Il n'existe pas de screen " + nbImage + " pour " + animeName)
        else:
            await sendEmbed(ctx, title, "Il existe aucun screen pour " + animeName)

    @commands.command(name="deleteAll")
    async def delete_all_command(self, ctx, *, animeName):
        if ctx.message.author.id == idBoss:
            destination = destFolder + animeName + separator
            # On regarde si une image existe pour l'anime
            if os.path.exists(destination):
                # message de confirmation
                await sendEmbed(ctx, ":warning: ALERTE ALERTE ALERTE :warning:",
                                "Etes-vous sûr de vouloir supprimer le dossier " + animeName + " ?")
                msg = await self.client.wait_for('message', check=lambda
                    message: message.author == ctx.author and message.channel.id == ctx.channel.id)
                yes = ["o", "oui", "y", "yes"]
                no = ["n", "non", "no"]
                if msg.content.lower() in yes:
                    # On supprime tout le dossier
                    shutil.rmtree(destination, ignore_errors=True)
                    await sendEmbed(ctx, "Tout supprimer pour " + animeName, "Dossier bien supprimé")
                elif msg.content.lower() in no:
                    # On annule la suppression
                    await sendEmbed(ctx, "Tout supprimer pour " + animeName, "Suppression annulée")
                else:
                    # On annule la suppression
                    await sendEmbed(ctx, "Tout supprimer pour " + animeName, "Réponse incorrect, suppression annulée")
            else:
                await sendEmbed(ctx, "Tout supprimer pour " + animeName, "Aucune dossier pour " + animeName)
        else:
            await sendEmbed(ctx, "Tout supprimer pour " + animeName,
                            "Qu'est-ce que tu essaies de faire là frérot ?????")

    @commands.command(name="deleteBetween")
    async def delete_between_command(self, ctx, start, end, *, animeName):
        title = "Suppresion des screens entre " + start + " et " + end + " pour " + animeName
        if ctx.message.author.id == idBoss:
            destination = destFolder + animeName + separator
            count = len([name for name in os.listdir(destination)])
            if count > 999:
                digits = 4
            else:
                digits = 3
            # On regarde si une image existe pour l'anime
            if os.path.exists(destination):
                # message de confirmation
                await sendEmbed(ctx, ":warning: ALERTE ALERTE ALERTE :warning:",
                                "Etes-vous sûr de vouloir supprimer les screens entre " + start + " et " + end + " pour " + animeName + " ?")
                msg = await self.client.wait_for('message', check=lambda
                    message: message.author == ctx.author and message.channel.id == ctx.channel.id)
                yes = ["o", "oui", "y", "yes"]
                no = ["n", "non", "no"]
                if msg.content.lower() in yes:
                    # On regarde si une image existe pour l'anime et si l'image avec l'index start et end existent aussi
                    if os.path.exists(destination) and os.path.exists(
                            destination + animeName + " - " + str(start).zfill(digits) + ".png") \
                            and os.path.exists(destination + animeName + " - " + str(end).zfill(digits) + ".png"):
                        await sendEmbed(ctx, title, "Début de la suppression")
                        # Récupération du nombre de fichier dans le dossier
                        nbImage = start
                        imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
                        while os.path.exists(imageName) and int(nbImage) <= int(end):
                            # On supprime l'image
                            os.remove(imageName)
                            nbImage = int(nbImage) + 1
                            imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"

                        # On renomme toutes les autres d'après si ce n'était pas la dernière
                        nbImage = int(end) + 1
                        count = int(start)
                        imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
                        await sendEmbed(ctx, title, "Début du renommage des screens")
                        while os.path.exists(imageName):
                            newName = destination + animeName + " - " + str(count).zfill(digits) + ".png"
                            os.rename(imageName, newName)
                            count += 1
                            nbImage += 1
                            imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
                        await sendEmbed(ctx, title, "Fin du renommage des screens")
                        await sendEmbed(ctx, title, "Fin de la suppression")
                    else:
                        await sendEmbed(ctx, title, "Il existe aucun screen pour " + animeName)
                    await sendEmbed(ctx, title, "Screens bien supprimés")
                elif msg.content.lower() in no:
                    # On annule la suppression
                    await sendEmbed(ctx, title, "Suppression annulée")
                else:
                    # On annule la suppression
                    await sendEmbed(ctx, title, "Réponse incorrect, suppression annulée")
            else:
                await sendEmbed(ctx, title, "Aucune dossier pour " + animeName)
        else:
            await sendEmbed(ctx, title, "Qu'est-ce que tu essaies de faire là frérot ?????")

    @commands.command(name="deleteDropbox")
    async def delete_dropbox_commande(self, ctx):
        await sendEmbed(ctx, "Suppression des fichiers Dropbox", "Début de la suppression")
        message = ""
        dbx = dropbox.Dropbox(oauth2_access_token=dropboxToken)
        files = dbx.files_list_folder("")
        for file in files.entries:
            message = message + file.name + "\n"
            dbx.files_delete_v2(file.path_display)
        if message == "":
            message = "Aucune fichier sur le dropbox"

        await sendEmbed(ctx, "Liste des fichiers supprimés", message)
