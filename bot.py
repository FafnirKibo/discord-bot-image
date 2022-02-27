from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        text = "    - save <anime> --> sauvegarde l'image attachée avec le nom de l'anime"
        text += "    - dest --> savoir le dossier de destination"
        text += "    - dLast <anime> --> supprime la dernière image de l'anime"
        await self.get_destination().send(text)
