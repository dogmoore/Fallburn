import yaml
import nextcord

from typing import Optional
from nextcord import slash_command, SlashOption
from nextcord.ext import commands

config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)


class Report_dropdown(nextcord.ui.Select):
    def __init__(self, mention, reporter, reason):
        self.target = mention
        self.reporter = reporter
        self.reason = reason
        options_array = [
            nextcord.SelectOption(label='Deny', description='Deny the report'),
            nextcord.SelectOption(label='Deny punishment', description='Accept the report but deny punishment'),
            nextcord.SelectOption(label='Mute', description='Accept and mute them for 1 hour'),
            nextcord.SelectOption(label='Kick', description='Accept and kick them'),
            nextcord.SelectOption(label='Ban', description='Accept and ban them')
        ]
        super().__init__(placeholder='Report options', min_values=1, max_values=1, options=options_array)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Deny':
            return await interaction.response.send_message(f'Denied {self.reporter}\'s report')

        if self.values[0] == 'Deny punishment':
            try:
                await self.reporter.send(
                    f'Your report was accept but staff chose not to issue a punishment against {self.target}')
            except Exception:
                pass
            return await interaction.response.send_message(
                f'Accepted {self.reporter}\'s report but did not punish {self.target}')

        if self.value[0] == 'Mute':  # 1 hour mute
            return

        if self.value[0] == 'Kick':
            return

        if self.value[0] == 'Ban':
            return


class Dropdown_render(nextcord.ui.View):
    def __init__(self, mention, reporter, reason):
        super().__init__()
        self.add_item(Report_dropdown(mention, reporter, reason))


class Anon(commands.Cog):
    def __init__(self, client):
        self.config = config
        self.client = client

    @slash_command(name='anonymous',
                   guild_ids=config['id']['guild'])
    async def anonymous(self, interaction: nextcord.Interaction):
        pass

    @anonymous.subcommand(name='confession',
                          description='Confess something anonymously')
    async def confess(self, interaction: nextcord.Interaction,
                      message: Optional[str] = SlashOption(required=True)):
        if self.config['module']['commands']['anon']:
            if not interaction.user.get_role(self.config['id']['mh_opt']):
                channel = self.client.get_channel(self.config['id']['confess_channel'])
                log = self.client.get_channel(self.config['id']['confess_log_channel'])

                confess_embed = nextcord.Embed(
                    title='Anonymous Confession',
                    description=message.capitalize(),
                    color=self.config['embed']['color']['default']
                )
                confess_embed.set_footer(text=self.config['embed']['footer'])

                confess_confirm_embed = nextcord.Embed(
                    title='Anonymous Confession Sent',
                    description='Your confession was sent',
                    color=self.config['embed']['color']['default']
                )
                confess_confirm_embed.set_footer(text=self.config['embed']['footer'])

                confess_log_embed = nextcord.Embed(
                    title=f'{interaction.user} | {interaction.user.display_name} sent a confession',
                    description=f'`{message}`',
                    color=self.config['embed']['color']['default']
                )

                await interaction.response.send_message(embed=confess_confirm_embed, ephemeral=True)
                await log.send(embed=confess_log_embed)
                await channel.send(embed=confess_embed)

    @anonymous.subcommand(name='save_me',
                          description='Privately get a list of resources to help with mental health either hidden in chat or in your DM')
    async def resources(self, interaction: nextcord.Interaction):
        await interaction.response.send_message('This command is still being created!')

    @slash_command(name='report',
                   description='Anonymously report another user',
                   guild_ids=config['id']['guild'])
    async def report(self, interaction: nextcord.Interaction,
                     mention: Optional[nextcord.Member] = SlashOption(required=True),
                     reason: Optional[str] = SlashOption(required=True),
                     evidence: Optional[str] = SlashOption(required=False)):
        report_channel = self.client.get_channel(self.config['id']['report_channel'])

        view = Dropdown_render(mention, interaction.user, reason)

        report_embed = nextcord.Embed(
            title=f'Report against {mention.name}#{mention.discriminator}',
            description=reason,
            color=self.config['embed']['color']['default']
        )

        report_embed.set_thumbnail(url=mention.avatar)
        report_embed.add_field(name='Reported by:', value=f'{interaction.user.name}#{interaction.user.discriminator}')
        report_embed.add_field(name='Evidence:', value=evidence)
        report_embed.set_footer(text=self.config['embed']['footer'])

        await report_channel.send(embed=report_embed, view=view)
        await interaction.response.send_message(
            content='Report has been filed!\nIf I am able to DM you, I will notify you about the results',
            ephemeral=True)


def setup(client):
    client.add_cog(Anon(client))
