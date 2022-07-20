import nextcord
import yaml
import random

from typing import Optional
from nextcord import slash_command, SlashOption
from nextcord.ext import commands

with open("./Configs/config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Kill(commands.Cog):
    def __init__(self, client):
        self.config = config
        self.array_length = len(self.config["kill_array"])

    @slash_command(name='kill',
                   description="Murder someone dead",
                   guild_ids=config["id"]["guild"]
                   )
    async def kill(self,
                   interaction: nextcord.Interaction,
                   mentions: Optional[nextcord.Member] = SlashOption(required=True)):
        print(self.array_length)
        msg = f'{interaction.user.name}{self.config["kill_array"][random.randint(0, self.array_length)]}{mentions}'
        await interaction.response.send_message(content=msg)


def setup(client):
    client.add_cog(Kill(client))
