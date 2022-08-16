import nextcord
import yaml

from nextcord import slash_command, SelectOption, Interaction
from nextcord.ext import commands

config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)


class DropdownMenu(nextcord.ui.Select):
    def __init__(self):
        self.config = config
        options_array = [
            SelectOption(label='World Wide | Internet Only'),
            SelectOption(label='United States'),
            SelectOption(label='United Kingdom')
        ]
        super().__init__(placeholder='Resource List Selection',
                         min_values=1,
                         max_values=1,
                         options=options_array)

    async def callback(self, interaction: Interaction):
        if self.values[0].lower() == 'world wide | internet only':

            internet_embed = nextcord.Embed(
                title='Internet only List',
                color=self.config['embed']['color']['default']
            )
            internet_embed.add_field(name='Religious Facebook group called We\'ll listen',
                                     value=f'[Jump to URL](https://m.facebook.com/profile.php?id=100052132313675)',
                                     inline=False)
            internet_embed.add_field(name='International OCD Foundation',
                                     value='[Jump to URL](https://iocdf.org/)',
                                     inline=False)

            await interaction.response.send_message(embed=internet_embed)
        if self.values[0].lower() == 'united states':

            usa_embed = nextcord.Embed(
                title='United States List',
                color=self.config['embed']['color']['default']
            )

            usa_embed.add_field(name='The Trevor Project',
                                value=f'[Jump to URL]( https://www.thetrevorproject.org/)',
                                inline=False)
            usa_embed.add_field(name='NIDA for drug abuse',
                                value='[Jump to URL](https://nida.nih.gov/)',
                                inline=False)
            usa_embed.add_field(name='NIAAA for alcohol abuse',
                                value='[Jump to URL](https://www.niaaa.nih.gov/)',
                                inline=False)
            usa_embed.add_field(name='National Suicide Prevention Hotline',
                                value='1-800-273-TALK (8255)',
                                inline=False)
            usa_embed.add_field(name='ADAA for anxiety and panic attacks',
                                value='[Jump to URL](https://adaa.org/understanding-anxiety/panic-disorder-agoraphobia/symptoms)',
                                inline=False)
            await interaction.response.send_message(embed=usa_embed)
        if self.values[0].lower() == 'united kingdom':

            uk_embed = nextcord.Embed(
                title='United Kingdom List',
                color=self.config['embed']['color']['default']
            )

            uk_embed.add_field(name='My Black Dog',
                               value='[Jump to URL](https://www.myblackdog.co/?gclid=Cj0KCQjw3eeXBhD7ARIsAHjssr9oU5KvaiTJEL7TO4cUQP7n13OcTuoLEpb6ZCefBJlsNa8IA91us4kaAtTCEALw_wcB)',
                               inline=False)
            uk_embed.add_field(name='Mind',
                               value='[Jump to URL](https://www.mind.org.uk/need-urgent-help/using-this-tool/)',
                               inline=False)
            uk_embed.add_field(name='Mind - continued',
                               value='[Jump to URL](https://www.mind.org.uk/information-support/guides-to-support-and-services/addiction-and-dependency/addiction-and-dependency-resources/)',
                               inline=False)
            uk_embed.add_field(name='URGENT\nSamaritans',
                               value='[Jump to URL](https://www.samaritans.org/how-we-can-help/contact-samaritan/)',
                               inline=False)

            await interaction.response.send_message(embed=uk_embed)


class DropdownRender(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMenu())


class ResListClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config

    @slash_command(name='help_me',
                   description='Gives a list of mental health resources in DM',
                   guild_ids=config['id']['guild'])
    async def help_me(self, interaction: Interaction):
        help_me_embed = nextcord.Embed(
            title='FallBurn\'s Mental Health Support',
            description='Please select your country, if it isn\'t listed then select `World Wide | Internet Only`\nWe have limited '
                        'resources so if your country isn\'t listed we can add it once we get even a single resources '
                        'for it',
            color=self.config['embed']['color']['default']
        )
        help_me_embed.set_footer(text=self.config['embed']['footer'])

        view = DropdownRender()

        try:
            await interaction.user.send(embed=help_me_embed, view=view)
            await interaction.response.send_message('I have sent you the form in your DM!', ephemeral=True)
        except Exception:
            await interaction.response.send_message('Please open your DM to me and run the command again!',
                                                    ephemeral=True)


def setup(client):
    client.add_cog(ResListClass(client))
