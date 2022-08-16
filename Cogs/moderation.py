import nextcord
import yaml
import datetime

from typing import Optional
from nextcord import slash_command, SlashOption, Permissions
from nextcord.ext import commands

config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config

    @slash_command(name='kick',  # TODO
                   default_member_permissions=Permissions(kick_members=True),
                   guild_ids=config['id']['guild'])
    async def kick(self, interaction: nextcord.Interaction,
                   mentions: Optional[nextcord.Member] = SlashOption(required=True),
                   reason: Optional[str] = SlashOption(required=True),
                   evidence: Optional[str] = SlashOption(required=False)):
        pass

    @slash_command(name='ban',  # TODO
                   default_member_permissions=Permissions(ban_members=True),
                   guild_ids=config['id']['guild'])
    async def ban(self, interaction: nextcord.Interaction,
                  mentions: Optional[nextcord.Member] = SlashOption(required=True),
                  reason: Optional[str] = SlashOption(required=True),
                  evidence: Optional[str] = SlashOption(required=True)):
        pass

    @slash_command(name='mute',  # TODO
                   default_member_permissions=Permissions(moderate_members=True),
                   guild_ids=config['id']['guild'])
    async def mute(self, interaction: nextcord.Interaction,  # TODO create embeds and log punishment
                   duration=SlashOption(
                       choices=[
                           '1 minute',
                           '5 minutes',
                           '10 minutes',
                           '30 minutes',
                           '1 hour',
                           '2 hours',
                           '5 hours',
                           '8 hours',
                           '12 hours',
                           '1 day',
                           '3 days',
                           '1 week',
                           '2 weeks',
                           '1 month'  # max is 28 days
                       ],
                       required=True
                   ),
                   target: Optional[nextcord.Member] = SlashOption(required=True),
                   reason: Optional[str] = SlashOption(required=True),
                   evidence: Optional[str] = SlashOption(required=False)):

        time_delta = datetime.timedelta(seconds=300)
        if duration == '1 minute':
            time_delta = datetime.timedelta(seconds=60)
        if duration == '5 minutes':
            time_delta = datetime.timedelta(seconds=300)
        if duration == '10 minutes':
            time_delta = datetime.timedelta(seconds=600)
        if duration == '30 minutes':
            time_delta = datetime.timedelta(seconds=1800)
        if duration == '1 hour':
            time_delta = datetime.timedelta(seconds=3600)
        if duration == '2 hours':
            time_delta = datetime.timedelta(seconds=7200)
        if duration == '5 hours':
            time_delta = datetime.timedelta(seconds=18000)
        if duration == '8 hours':
            time_delta = datetime.timedelta(seconds=28800)
        if duration == '12 hours':
            time_delta = datetime.timedelta(seconds=43200)
        if duration == '1 day':
            time_delta = datetime.timedelta(days=1)
        if duration == '3 days':
            time_delta = datetime.timedelta(days=3)
        if duration == '1 week':
            time_delta = datetime.timedelta(days=7)
        if duration == '2 weeks':
            time_delta = datetime.timedelta(days=14)
        if duration == '1 month':
            time_delta = datetime.timedelta(days=28)
        try:
            mute_embed = nextcord.Embed(
                title=f'{target.user} got muted for {duration}',
                description=f'Reason: {reason}',
                color=self.config['embed']['color']['default']
            )
            mute_embed.set_footer(text=self.config['embed']['footer'])

            mute_log_embed = nextcord.Embed(
                title='Mute log',
                description=f'{target.user} for muted for {duration}',
                color=self.config['embed']['color']
            )

            await target.edit(timeout=nextcord.utils.utcnow() + time_delta)
            await interaction.response.send_message(embed=mute_embed)
        except Exception as err:
            await interaction.response.send_message('I can not mute this person')


def setup(client):
    client.add_cog(Moderation(client))
