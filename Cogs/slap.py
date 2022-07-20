import nextcord
import yaml

from typing import Optional
from nextcord import slash_command, SlashOption
from nextcord.ext import commands

with open("./Configs/config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Slap(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config

    @slash_command(name='slap',
                   description="Slap someone",
                   guild_ids=config["id"]["guild"]
                   )
    async def slap(self,
                   interaction: nextcord.Interaction,
                   mentions: Optional[nextcord.Member] = SlashOption(required=False)):
        if mentions is None:
            return await interaction.response.send_message(content=f'{interaction.user.name} slapped themself')
        await interaction.response.send_message(content=f'{mentions[:-5]} got slapped')


def setup(client):
    client.add_cog(Slap(client))
