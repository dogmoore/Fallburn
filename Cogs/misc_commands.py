import nextcord
import yaml
import random
import requests
import json


from typing import Optional
from nextcord import slash_command, SlashOption
from nextcord.ext import commands

config = yaml.load(open("./Configs/config.yml", 'r'), Loader=yaml.FullLoader)


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config
        try:
            self.kill_array_length = len(self.config["msg_arrays"]["kill"])
            self.hug_array_length = len(self.config["msg_arrays"]["hug"])
        except Exception as error:
            print(error)
            self.kill_array_length = 1
            self.hug_array_length = 1

    @slash_command(name='kill',
                   description="Murder someone dead",
                   guild_ids=config["id"]["guild"])
    async def kill(self,
                   interaction: nextcord.Interaction,
                   mentions: Optional[nextcord.Member] = SlashOption(required=True)):
        if self.config['module']['commands']['fun']:
            kill_array_msg = self.config["msg_arrays"]["kill"][random.randint(0, self.kill_array_length)]
            msg = f'{interaction.user.name}{kill_array_msg}{mentions.mention}'
            try:
                await interaction.response.send_message(content=msg)
            except Exception as error:
                print(error)
                await interaction.response.send_message(
                    content=f'{interaction.user.name} fucking stabbed {mentions.mention}')

    @slash_command(name='hug',
                   description='Hug someone',
                   guild_ids=config["id"]['guild'])
    async def hug(self,
                  interaction: nextcord.Interaction,
                  mentions: Optional[nextcord.Member] = SlashOption(required=True)):
        if self.config['module']['commands']['fun']:
            hug_array_msg = self.config["msg_arrays"]["hug"][random.randint(0, self.hug_array_length)]
            msg = f'{interaction.user.name}{hug_array_msg}{mentions.mention}'
            try:
                await interaction.response.send_message(content=msg)
            except Exception as error:
                print(error)
                await interaction.response.send_message(
                    content=f'{interaction.user.name} fucking hugged {mentions.mention}')

    @slash_command(name='slap',
                   description="Slap someone",
                   guild_ids=config["id"]["guild"])
    async def slap(self,
                   interaction: nextcord.Interaction,
                   mentions: Optional[nextcord.Member] = SlashOption(required=False)):
        if self.config['module']['commands']['fun']:
            if mentions is None:
                return await interaction.response.send_message(content=f'{interaction.user.name} slapped themself')
            await interaction.response.send_message(content=f'{mentions} got slapped')

    @slash_command(name='ping',
                   description="Ping the server",
                   guild_ids=config["id"]["guild"]
                   )
    async def ping(self,
                   interaction: nextcord.Interaction):
        if self.config['module']['commands']['general']:
            ping_embed = nextcord.Embed(
                description=f'Latency: `{round(interaction.client.latency * 1000)}`ms',
                color=self.config['embed']['color']['default']
            )
            ping_embed.set_footer(text=self.config["embed"]["footer"])
            await interaction.response.send_message(embed=ping_embed)

    @slash_command(name='urban',
                   description='Search urban dictionary',
                   guild_ids=config["id"]["guild"]
                   )
    async def urban(self, interaction: nextcord.Interaction,
                    message: Optional[str] = SlashOption(required=True)):
        if self.config['module']['commands']['fun']:
            response = requests.get(f"http://api.urbandictionary.com/v0/define?term={message}")
            dictionary = json.loads(response.text)['list']
            most_thumbs = -1
            best_definition = ""
            for definition in dictionary:
                if definition['thumbs_up'] > most_thumbs:
                    most_thumbs = definition['thumbs_up']
                    best_definition = definition['definition']
            urban_embed = nextcord.Embed(
                title=f'{message.capitalize()} Definition:',
                description=f'{best_definition}',
                color=self.config['embed']['color']['default']
            )
            urban_embed.set_footer(text=self.config["embed"]['footer'])
            urban_embed.set_image(self.config['images']['urban'])
            await interaction.response.send_message(embed=urban_embed)

    @slash_command(name='suggest',
                    description='Suggest a change for the server',
                    guild_ids=config['id']['guild'])
    async def suggest(self, interaction: nextcord.Interaction, suggestion: Optional[str] = SlashOption(required=True)):
        suggest_channel = self.client.get_channel(self.config['id']['suggestion_channel'])
        
        suggest_embed = nextcord.Embed(
            title=f'suggestion by {interaction.user}',
            description=suggestion,
            color=self.config['embed']['color']['default']
        )

        suggest_embed.set_footer(text=self.config['embed']['footer'])
        await suggest_channel.send(embed=suggest_embed)
        await interaction.response.send_message('Your suggestion has been made', ephemeral=True)

def setup(client):
    client.add_cog(Misc(client))
