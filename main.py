import os
import random
import zipfile

import discord
import dropbox
from discord.ext import commands

import variable

# from win10toast import ToastNotifier

client = commands.Bot(command_prefix='.')
token = variable.token
destFolder = variable.winDest
separator = "\\"
dropboxToken = variable.dropboxToken


# toast = ToastNotifier()
# toast.show_toast("Bot Image Sauvegarde", "Le programme a été lancé", duration=30)

# os.chdir("D:\Projets\sauvegardeImages")


@client.event
async def on_ready():
    print("Bot is ready")
    print(token)


@client.command()
async def save(ctx, *, animeName):
    try:
        destination = destFolder + animeName + separator

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
    destination = destFolder + animeName + separator

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
    destination = destFolder + animeName + separator

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
async def send(ctx, userID, nbImage, *, animeName):
    destination = destFolder + animeName + separator
    user = client.get_user(userID) or await client.fetch_user(userID)

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération de l'image
        imageName = animeName + " - " + str(nbImage).zfill(3) + ".png"
        if os.path.exists(destination + imageName):
            # Envoie de l'image
            await user.send(animeName + " " + nbImage + " :")
            await user.send(file=discord.File(destination + imageName))
            await alert(ctx, "Image '" + imageName + "' bien envoyée à " + user.name + " !")
        else:
            await ctx.send("Il n'existe pas d'image " + nbImage + " pour l'anime : " + animeName)
    else:
        await alert(ctx, "Aucune image existe pour l'anime : " + animeName)


@client.command()
async def sendFrom(ctx, userID, nbImage, *, animeName):
    destination = destFolder + animeName + separator
    user = client.get_user(userID) or await client.fetch_user(userID)

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération de l'image
        imageName = animeName + " - " + str(nbImage).zfill(3) + ".png"
        if os.path.exists(destination + imageName):
            # Création du ZIP
            archiveName = animeName + "_" + user.name + ".zip"
            zipObj = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
            # Envoie de l'image
            await user.send(animeName + " depuis l'image " + nbImage + " :")
            await user.send(file=discord.File(destination + imageName))
            zipObj.write(destination + imageName, arcname=imageName)
            await alert(ctx, "Image '" + imageName + "' bien envoyée à " + user.name + " !")
            # On continue à envoyer si il en reste
            count = int(nbImage) + 1
            imageName = animeName + " - " + str(count).zfill(3) + ".png"
            while os.path.exists(destination + imageName):
                await user.send(file=discord.File(destination + imageName))
                # Ajout de l'image à l'archive
                zipObj.write(destination + imageName, arcname=imageName)
                await alert(ctx, "Image '" + imageName + "' bien envoyée à " + user.name + " !")
                count += 1
                imageName = animeName + " - " + str(count).zfill(3) + ".png"
            zipObj.close()
            await saveDropbox(ctx, archiveName, user)
        else:
            await ctx.send("Il n'existe pas d'image " + nbImage + " pour l'anime : " + animeName)
    else:
        await alert(ctx, "Aucune image existe pour l'anime : " + animeName)


@client.command()
async def sendFromTo(ctx, userID, nbImageFrom, nbImageTo, *, animeName):
    destination = destFolder + animeName + separator
    user = client.get_user(userID) or await client.fetch_user(userID)

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération de l'image
        imageName = animeName + " - " + str(nbImageFrom).zfill(3) + ".png"
        if os.path.exists(destination + imageName):
            # Création du ZIP
            archiveName = animeName + "_" + user.name + ".zip"
            zipObj = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
            # Envoie de l'image
            await user.send(
                animeName + " depuis l'image " + nbImageFrom + " à l'image " + nbImageTo + " (si elle existe) :")
            await user.send(file=discord.File(destination + imageName))
            zipObj.write(destination + imageName, arcname=imageName)
            await alert(ctx, "Image '" + imageName + "' bien envoyée à " + user.name + " !")
            # On continue à envoyer si il en reste
            count = int(nbImageFrom) + 1
            imageName = animeName + " - " + str(count).zfill(3) + ".png"
            while os.path.exists(destination + imageName) and count <= int(nbImageTo):
                await user.send(file=discord.File(destination + imageName))
                # Ajout de l'image à l'archive
                zipObj.write(destination + imageName, arcname=imageName)
                await alert(ctx, "Image '" + imageName + "' bien envoyée à " + user.name + " !")
                count += 1
                imageName = animeName + " - " + str(count).zfill(3) + ".png"
            zipObj.close()
            await saveDropbox(ctx, archiveName, user)
        else:
            await ctx.send("Il n'existe pas d'image " + nbImageFrom + " pour l'anime : " + animeName)
    else:
        await alert(ctx, "Aucune image existe pour l'anime : " + animeName)


async def saveDropbox(ctx, file, user):
    dbx = dropbox.Dropbox(oauth2_access_token=dropboxToken)
    n = random.randint(0, 10000)
    with open(file, 'rb') as f:
        dbx.files_upload(f.read(), '/' + str(n) + '-' + file)
    link = dbx.sharing_create_shared_link_with_settings('/' + str(n) + '-' + file)
    await user.send("Archive des screens : " + str(link.url))
    await alert(ctx, "Archive '" + file + "' bien envoyée à " + user.name + " !")
    os.remove(file)


@client.command()
async def show(ctx, nbImage, *, animeName):
    destination = destFolder + animeName + separator

    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        # Récupération de l'image
        imageName = animeName + " - " + str(nbImage).zfill(3) + ".png"
        url = destination + imageName
        if os.path.exists(url):
            # Envoie du message avec l'image
            file = discord.File(url)
            embed = discord.Embed(title=imageName, color=discord.Color.blue())
            embed.set_image(url="attachment://" + url)
            await ctx.send(file=file, embed=embed)
        else:
            embed = discord.Embed(title="Pas de screen " + nbImage + " pour " + animeName, color=discord.Color.blue())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Pas de screen pour " + animeName, color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.command()
async def search(ctx, *, animeName):
    result = ""

    for folderName in os.listdir(destFolder):
        folder = os.path.join(destFolder, folderName)
        if os.path.isdir(folder) and (animeName.lower() in folderName.lower()):
            result = result + folderName + "\n"
    if result == "":
        result = "Aucun résultat trouvé"
    embed = discord.Embed(title="Liste des résultats", description=result, color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def searchAll(ctx):
    result = ""

    for folderName in os.listdir(destFolder):
        folder = os.path.join(destFolder, folderName)
        if os.path.isdir(folder):
            result = result + folderName + "\n"
    if result == "":
        result = "Aucun résultat trouvé"
    embed = discord.Embed(title="Tout les résultats", description=result, color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def count(ctx, *, animeName):
    destination = destFolder + animeName + separator
    count = 0
    # On regarde si une image existe pour l'anime
    if os.path.exists(destination):
        count = len([name for name in os.listdir(destination)])
    embed = discord.Embed(title="Nombre de screen pour " + animeName, description=count, color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def deleteDropbox(ctx):
    message = ""
    dbx = dropbox.Dropbox(oauth2_access_token=dropboxToken)
    files = dbx.files_list_folder("")
    for file in files.entries:
        message = message + file.name + "\n"
        dbx.files_delete_v2(file.path_display)
    embed = discord.Embed(title="Liste des fichiers supprimés", description=message, color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def move(ctx, ancientFolder, ancientName, newFolder, newName):
    yes = 1


async def alert(ctx, msg):
    print(msg)
    await ctx.send(msg)


client.run(token)
