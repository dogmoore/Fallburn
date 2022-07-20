import os
import nextcord
import yaml

from nextcord.ext import commands
from nextcord.ext.application_checks import errors as application_errors
from nextcord.ext.commands import Bot

config = yaml.load(open("./Configs/config.yml", 'r'), Loader=yaml.FullLoader)


class Fallburn(commands.Bot):
    def __init__(self):

        self.config = config

        intents = nextcord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.presences = True
        intents.message_content = True

        activity = nextcord.Activity(name=self.config["activity_msg"], type=nextcord.ActivityType.playing)

        super().__init__(
            command_prefix='>>',
            help_command=None,
            bot_owner=self.config["id"]["owner"],
            activity=activity,
            intents=intents,
            case_insensitive=True
        )

        for i in os.listdir('Cogs'):
            if i.endswith('.py'):
                try:
                    Bot.load_extension(self, name=f'Cogs.{i[:-3]}')
                    print(f'Cog {i[:-3]}')
                except Exception as error:
                    print(error)

    async def on_ready(self):
        print('(Pterodactyl Bot Online)')

    # error handling
    async def on_command_error(self, ctx, error):
        error_embed = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.",
            color=self.config["embed"]["color"]
        )

        if isinstance(error, commands.errors.MissingRequiredArgument):
            error_embed.add_field(
                name="Error is described below.",
                value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```"
            )
            error_embed.set_footer(text=self.config["embed"]["footer"])
            return await ctx.send(embed=error_embed)
        # self.logger.critical(f'Something went wrong, {error}')

    async def on_application_command_error(self, interaction: nextcord.Interaction, error: Exception):
        if isinstance(error, application_errors.ApplicationMissingRole):
            role = interaction.guild.get_role(int(error.missing_role))
            return await interaction.send(f"{role.mention} role is required to use this command.", ephemeral=True)
        await interaction.send(f"This command raised an exception: `{type(error)}:{str(error)}`", ephemeral=True)
        return  # self.logger.error(str(error))

