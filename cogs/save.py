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
        title = "Sauvegardes de screen pour " + animeName
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
            imageName = animeName + " - " + str(count).zfill(3) + ".png"
            # Enregistrement de l'image
            await ctx.message.attachments[0].save(destination + imageName)
            await sendEmbed(ctx, "Screen bien sauvegardé dans", destination + imageName)
        else:
            await sendEmbed(ctx, title, "Pas de screen attaché au message")

    @commands.command(name='saveAll')
    async def save_multiple_command(self, ctx, *, animeName):
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
            # Enregistrement des screens
            description = ""
            for screen in ctx.message.attachments:
                imageName = animeName + " - " + str(count).zfill(3) + ".png"
                description = description + imageName + "\n"
                await screen.save(destination + imageName)
                count += 1
            await sendEmbed(ctx, "Sauvegarde des screens suivants", description)
        else:
            await sendEmbed(ctx, title, "Pas de screen attaché au message")
