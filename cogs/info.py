from discord.ext import commands

from main import destFolder


def setup(client):
    client.add_cog(Info(client))


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="dest")
    async def destination_command(self, ctx):
        await ctx.send("Dossier de destination : " + destFolder)

    @commands.command(name="test")
    async def test_commande(self, ctx, test1, test2):
        await ctx.send("TEST !! Test 1 = " + test1 + " test 2 = " + test2)
