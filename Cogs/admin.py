import nextcord
import yaml

from typing import Optional
from nextcord import slash_command, SlashOption, user_command, Permissions
from nextcord.ext import commands

# from Utils.db import DB

config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config

    @slash_command(name='say',
                   guild_ids=config["id"]["guild"],
                   default_member_permissions=Permissions(administrator=True))
    @commands.is_owner()
    async def say_main(self, interaction: nextcord.Interaction):
        pass

    @say_main.subcommand(name='text',
                         description='Make the bot say text | BOT OWNER ONLY')
    @commands.is_owner()
    async def text(self, interaction: nextcord.Interaction,
                   message: Optional[str] = SlashOption(required=True)):
        if self.config['module']['commands']['admin'] and interaction.user.id == self.config['id']['owner']:
            await interaction.response.send_message(content="Sent!", ephemeral=True, delete_after=2)
            channel = self.client.get_channel(interaction.channel_id)
            await channel.send(content=message)

    @say_main.subcommand(name='embed',
                         description='Make the bot say an embed | BOT OWNER ONLY')
    @commands.is_owner()
    async def embed(self, interaction: nextcord.Interaction,
                    title: str,
                    description: Optional[str] = SlashOption(required=False)):
        if self.config['module']['commands']['admin'] and interaction.user.id == self.config['id']['owner']:
            if description is None: description = ' '
            say_embed = nextcord.Embed(
                title=title,
                description=description,
                color=self.config["embed"]["color"]['default']
            )
            await interaction.response.send_message(content="Sent!", ephemeral=True, delete_after=2)
            channel = self.client.get_channel(interaction.channel_id)
            await channel.send(embed=say_embed)

    # @slash_command(name='admin',
    #                guild_ids=config['id']['guild'])
    # @commands.is_owner()
    # async def admin(self, interaction: nextcord.Interaction):
    #     pass
    #
    # @admin.subcommand(name='database_setup', description='ran to set up database | BOT OWNER ONLY')
    # @commands.is_owner()
    # async def setup(self, interaction: nextcord.Interaction):
    #     log_channel = self.client.get_channel(self.config['id']['log_channel'])
    #     await interaction.response.send_message(content='Adding users to database...')
    #     await DB.setup()
    #     await log_channel.send(content='Finished creating the tables')


def setup(client):
    client.add_cog(Admin(client))
