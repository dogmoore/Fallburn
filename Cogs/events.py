import time
import yaml

from nextcord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.logger = self.client.logger
        self.config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)
        # self.ignored_channels = self.config["id"]["ignored_channels"]

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
        # if self.config["modules"]["invite_detection"]:
        #     if 'https://discord.gg/' in message.content:  # invite detection
        #         time.sleep(0.5)  # to prevent bad packets
        #         if not message.author.bot:
        #             if message.channel.id not in self.ignored_channels:
        #                 msg = message.content()
        #                 author = message.author
        #                 # await message.delete()
        #                 # await message.channel.send(f'{author} please do not sent discord invites')
        #                 await message.edit(content=self.config["invite"])


def setup(client):
    client.add_cog(Events(client))
