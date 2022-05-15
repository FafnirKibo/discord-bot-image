import os

from discord.ext import commands

from main import destFolder, separator, sendEmbed


def setup(client):
    client.add_cog(Save(client))


class Save(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='save')
    async def save_command(self, ctx, *, animeName):
        title = "Sauvegardes des screens pour " + animeName
        if ctx.message.attachments:
            destination = destFolder + animeName + separator

            # Création du dossier de l'anime si besoin
            if not os.path.exists(destination):
                await sendEmbed(ctx, title, "Il existe aucun dossier pour " + animeName)
                try:
                    os.makedirs(destination)
                    await sendEmbed(ctx, title, "Création du dossier réussi")
                except:
                    await sendEmbed(ctx, title, "Echec de la création du dossier")

            # Récupération du nombre de fichier dans le dossier
            count = len([name for name in os.listdir(destination)]) + 1
            if count > 999:
                digits = 4
            else:
                digits = 3
            # Enregistrement des screens
            description = ""
            for screen in ctx.message.attachments:
                # Si on arrive à 1000, on renomme les autres images avec 4 digits
                if count == 1000:
                    await sendEmbed(ctx, title, "Compte arrivé à 1000, début du renommage des screens en 4 digits")
                    newCount = 1
                    previousName = destination + animeName + " - " + str(newCount).zfill(3) + ".png"
                    while os.path.exists(previousName) and newCount < 1000:
                        newName = destination + animeName + " - " + str(newCount).zfill(4) + ".png"
                        os.rename(previousName, newName)
                        newCount += 1
                        previousName = destination + animeName + " - " + str(newCount).zfill(3) + ".png"
                    await sendEmbed(ctx, title, "Fin du renommage des screens en 4 digits")

                imageName = animeName + " - " + str(count).zfill(digits) + ".png"
                description = description + imageName + "\n"
                await screen.save(destination + imageName)
                count += 1
            await sendEmbed(ctx, "Sauvegarde des screens suivants", description)
        else:
            await sendEmbed(ctx, title, "Pas de screen attaché au message")
