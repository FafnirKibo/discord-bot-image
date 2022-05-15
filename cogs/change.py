import os

from discord.ext import commands

from main import destFolder, separator, sendEmbed


def setup(client):
    client.add_cog(Change(client))


class Change(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="move")
    async def move_command(self, ctx, ancientFolder, ancientName, animeName):
        # L'ancien dossier et le nouveau
        ancientDest = destFolder + ancientFolder + separator
        newDest = destFolder + animeName + separator
        # Titre pour le embed
        title = "Déplacement de " + ancientDest + " dans " + newDest
        # On regarde si l'ancien dossier existe au moins
        if os.path.exists(ancientDest):
            count = 1
            count = len([name for name in os.listdir(ancientDest)])
            if count > 999:
                digits = 4
            else:
                digits = 3
            imageName = ancientDest + ancientName + " - " + str(count).zfill(digits) + ".png"
            # On regarde s'il y a au moins une image dans l'ancien dossier
            if os.path.exists(imageName):
                newCount = 1
                # On regarde si le nouveau dossier existe deja, sinon on le crée
                if os.path.exists(newDest):
                    newCount = len([name for name in os.listdir(newDest)]) + 1
                    await sendEmbed(ctx, "Nouveau dossier " + animeName, "Dossier deja existant")
                else:
                    try:
                        os.makedirs(newDest)
                        await sendEmbed(ctx, "Nouveau dossier " + animeName, "Création du dossier " + animeName)
                    except:
                        await sendEmbed(ctx, "Nouveau dossier " + animeName,
                                        "Erreur lors de la création du dossier " + animeName)

                # On boucle sur les screen et on les déplace
                while os.path.exists(imageName):
                    newName = newDest + animeName + " - " + str(int(newCount)).zfill(digits) + ".png"
                    os.rename(imageName, newName)
                    count += 1
                    newCount += 1
                    imageName = ancientDest + ancientName + " - " + str(count).zfill(digits) + ".png"

                # Si après déplacement, l'ancien dossier ne contient plus rien, on le supprime
                if len([name for name in os.listdir(ancientDest)]) == 0:
                    os.rmdir(ancientDest)
                    await sendEmbed(ctx, "Ancient dossier " + ancientFolder + " supprimé", "Plus aucun screen dedans")
                description = "Fin de déplacement des screen"

            else:
                description = "Aucun screen pour l'anime " + ancientName + " dans " + ancientFolder
        else:
            description = "Aucun dossier " + ancientFolder + " trouvé"
        await sendEmbed(ctx, title, description)

    @commands.command(name="rename")
    async def rename_command(self, ctx, ancientName, newName):
        destination = destFolder + ancientName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3
        # Titre pour le embed
        title = "Renommage de " + ancientName + " en " + newName
        # On regarde si l'ancien dossier existe au moins
        if os.path.exists(destination):
            count = 1
            imageName = destination + ancientName + " - " + str(count).zfill(digits) + ".png"
            # On regarde s'il y a au moins une image dans l'ancien dossier
            if os.path.exists(imageName):
                # On boucle sur les screen et on les renomme
                while os.path.exists(imageName):
                    newImageName = destination + newName + " - " + str(int(count)).zfill(digits) + ".png"
                    os.rename(imageName, newImageName)
                    count += 1
                    imageName = destination + ancientName + " - " + str(count).zfill(digits) + ".png"
                description = "Fin du renommage des screen"
                await sendEmbed(ctx, title, description)

                # Nouveau nom du dossier
                newDest = destFolder + newName + separator
                os.rename(destination, newDest)
                description = "Fin du renommage du dossier"
                await sendEmbed(ctx, title, description)
            else:
                description = "Aucun screen pour l'anime " + ancientName + " à renommer"
                await sendEmbed(ctx, title, description)
        else:
            description = "Aucun dossier " + ancientName + " trouvé"
            await sendEmbed(ctx, title, description)

    @commands.command(name="resetName")
    async def reset_name_command(self, ctx, *, animeName):
        title = "Reset des noms des screens de " + animeName
        destination = destFolder + animeName + separator
        count = len([name for name in os.listdir(destination)])
        if count > 999:
            digits = 4
        else:
            digits = 3
        # Récupération du numéro du premier screen
        nbImage = 1
        imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
        while not os.path.exists(imageName):
            nbImage += 1
            imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
        count = 1
        await sendEmbed(ctx, title, "Début du renommage des screens")
        while os.path.exists(imageName):
            newName = destination + animeName + " - " + str(count).zfill(digits) + ".png"
            os.rename(imageName, newName)
            count += 1
            nbImage += 1
            imageName = destination + animeName + " - " + str(nbImage).zfill(digits) + ".png"
        await sendEmbed(ctx, title, "Fin du renommage des screens")
