import os
import nextcord
import yaml

from nextcord.ext import commands
from nextcord.ext.commands import Bot

config = yaml.load(open("./Configs/config.yml", 'r'), Loader=yaml.FullLoader)

loaded_cogs = []


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
            #bot_owner=self.config["id"]["owner"],
            activity=activity,
            intents=intents,
            case_insensitive=True
        )

        for i in os.listdir('Cogs'):
            if i.endswith('.py'):
                Bot.load_extension(self, name=f'Cogs.{i[:-3]}')
                loaded_cogs.append({i})

    async def on_ready(self):

        def enabled_check(is_enabled):
            if is_enabled:
                return 'ENABLED'
            return 'DISABLED'

        for i in os.listdir('Cogs'):
            if i.endswith('.py') and loaded_cogs:
                print(f'Cog {i[:-3]} Loaded')
            if i.endswith('.py') and not loaded_cogs:
                print(f'Cog {i[:-3]} Failed to Load')
        
        print(f'\nwelcome message: {enabled_check(config["module"]["welcome"])}')
        print(f'events: {enabled_check(config["module"]["events"])}')
        print(f'commands: fun {enabled_check(config["module"]["commands"]["fun"])}')
        print(f'commands: anon {enabled_check(config["module"]["commands"]["anon"])}')
        print(f'commands: general {enabled_check(config["module"]["commands"]["general"])}')
        print(f'commands: admin {enabled_check(config["module"]["commands"]["admin"])}')

        print('(Pterodactyl Bot Online)')
