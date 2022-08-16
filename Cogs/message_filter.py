import nextcord
import yaml
import re

from nextcord.ext import commands


class Filter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)
        self.words = self.config["filter_list"]

    # @commands.Cog.listener()
    # async def on_message(self, msg):  # message log
    #     if self.config['module']['log']['message'] and self.config['module']['events']:

    #         def useRegex(input):
    #             pattern = re.compile(r"fag fag1t faget fagg1t faggit faggot fagit fags fagz faig faigs n1gr nastt nigger nigur niiger niigr nigga", re.IGNORECASE)
    #             return pattern.match(input)

    #         log_channel = self.client.get_channel(self.config['id']['log_channel'])
    #         for x in self.words:
    #             if msg.content.includes(x):
    #                 log_channel.send(content='Hit!')
    #                 break


def setup(client):
    client.add_cog(Filter(client))