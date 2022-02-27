import os

import discord
from discord.ext import commands
from win10toast import ToastNotifier

import variable

client = commands.Bot(command_prefix='.')
token = variable.token
destFolder = "D:\\Images\\Screen_Anime\\"

toast = ToastNotifier()
toast.show_toast("Bot Image Sauvegarde", "Le programme a été lancé", duration=30)

os.chdir("D:\Projets\sauvegardeImages")


@client.event
async def on_ready():
    print("Bot is ready")
    print(token)


@client.command()
async def save(ctx, *, animeName):
    try:
        destination = destFolder + animeName + '\\'

        # Création du dossier de l'anime si besoin
        if not os.path.exists(destination):
            await alert(ctx, "Il existe aucun dossier pour l'anime : " + animeName)
            try:
                os.makedirs(destination)
                await alert(ctx, "Création du dossier pour l'anime : " + animeName + " réussi")
            except:
                await alert(ctx, "Echec de la création du dossier pour l'anime : " + animeName)

        # Récupération du nombre de fichier dans le dossier
        count = len([name for name in os.listdir(destination)]) + 1
        imageName = animeName + " - " + str(count).zfill(3) + ".png"
        # Enregistrement de l'image
        await ctx.message.attachments[0].save(destination + imageName)
        await alert(ctx, "Image bien sauvegardée dans : " + destination + imageName + " !")
    except IndexError:
        print("Pas d'image attachée au message")
        await ctx.send("Pas d'image attachée au message!")


@client.command()
async def test(ctx):
    await ctx.send("TEST !!")


@client.command()
async def dest(ctx):
    await ctx.send("Dossier de destination : " + destFolder)


@client.command()
async def dLast(ctx, *, animeName):
    destination = destFolder + animeName + '\\'

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération du nombre de fichier dans le dossier
        count = len([name for name in os.listdir(destination)])
        imageName = animeName + " - " + str(count).zfill(3) + ".png"
        if os.path.exists(destination + imageName):
            os.remove(destination + imageName)
            await alert(ctx, "Image bien supprimée : " + destination + imageName + " !")
        else:
            await ctx.send("Le dossier existe mais il y a aucune image pour l'anime : " + animeName)
    else:
        await alert(ctx, "Aucune image existe pour l'anime : " + animeName)


@client.command()
async def dl(ctx, animeName, nbImage):
    destination = destFolder + animeName + '\\'

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération du nombre de fichier dans le dossier
        imageName = animeName + " - " + str(nbImage).zfill(3) + ".png"
        if os.path.exists(destination + imageName):
            # On supprime l'image
            os.remove(destination + imageName)
            await alert(ctx, "Image bien supprimée : " + destination + imageName + " !")
            # On renomme toutes les autres d'après si ce n'était pas la dernière
            count = int(nbImage) + 1
            imageName = destination + animeName + " - " + str(count).zfill(3) + ".png"
            while os.path.exists(imageName):
                newName = destination + animeName + " - " + str(int(count) - 1).zfill(3) + ".png"
                os.rename(imageName, newName)
                count += 1
                imageName = destination + animeName + " - " + str(count).zfill(3) + ".png"
                await alert(ctx, "Image bien renommée : " + newName + " !")
        else:
            await ctx.send("Il n'existe pas d'image " + nbImage + " pour l'anime : " + animeName)
    else:
        await alert(ctx, "Aucune image existe pour l'anime : " + animeName)


@client.command()
async def send(ctx, userID, animeName, nb):
    user = client.get_user(userID) or await client.fetch_user(userID)
    await user.send(file=discord.File(destFolder + 'Gintama - 001.png'))

    imageName = destFolder + animeName + ' - ' + str(nb).zfill(3) + ".png"
    if os.path.exists(destFolder + imageName):
        os.remove(destFolder + imageName)
        print('Image supprimée : ' + imageName)
        await ctx.send("Image bien supprimée : " + destFolder + imageName + " !")
    else:
        print("Il existe aucune image pour l'anime : " + animeName)
        await ctx.send("Il existe aucune image pour l'anime : " + animeName)


async def alert(ctx, msg):
    print(msg)
    await ctx.send(msg)


client.run(token)
