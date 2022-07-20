import nextcord
import yaml

from nextcord import slash_command
from nextcord.ext import commands

with open("./Configs/config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config

    @slash_command(name='ping',
                   description="Ping the server",
                   guild_ids=config["id"]["guild"]
                   )
    async def ping(self, interaction: nextcord.Interaction):
        ping_embed = nextcord.Embed(
            description=f'Latency: `{round(interaction.client.latency * 1000)}`ms',
            color=self.config['embed']['color']
        )
        ping_embed.set_footer(text=self.config["embed"]["footer"])
        await interaction.response.send_message(embed=ping_embed)


def setup(client):
    client.add_cog(Ping(client))
