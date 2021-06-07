import os

from discord.ext import commands

client = commands.Bot(command_prefix='.')
token = "ODUxMTI4MzI4MTM5MTc4MDY1.YLzxBg.DjvTZd3AFj5SZHTyPBmijH7UYws"
destFolder = "D:\\Images\\Printemps 2021\\"


@client.event
async def on_ready():
    print("Bot is ready")
    print(token)


@client.command()
async def save(ctx, *, animeName):
    try:
        # On regarde le nombre d'image avec le même nom pour le nom
        count = 0
        for root, dirs, files in os.walk(destFolder):
            for filename in files:
                if filename.startswith(animeName):
                    count += 1
        count += 1
        imageName = animeName + " - " + str(count).zfill(3) + ".png"
        await ctx.message.attachments[0].save(destFolder + imageName)
        print('Image sauvegardée: ' + imageName)
        await ctx.send("Image bien sauvegardée dans : " + destFolder + imageName + " !")
    except IndexError:
        print("Pas d'image attachée au message")
        await ctx.send("Pas d'image attachée au message!")


@client.command()
async def test(ctx):
    await ctx.send("TEST !!")


client.run(token)
