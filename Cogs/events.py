import nextcord
import yaml

from nextcord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = yaml.load(open("./Configs/config.yml", "r"), Loader=yaml.FullLoader)
        # log_channel = self.client.get_channel(self.config['id']['log_channel'])
        # self.welcome_channel = self.client.get_channel(self.config['id']['hidden_welcome_channel'])
        # self.general = self.client.get_channel(self.config['id']['general'])

    @commands.Cog.listener()
    async def on_message_delete(self, deleted_msg):  # message log
        if self.config['module']['log']['message'] and self.config['module']['events']:
            if not deleted_msg == '':  # removes deleted embeds

                log_channel = self.client.get_channel(self.config['id']['log_channel'])

                delete_embed = nextcord.Embed(
                    title=f'Member {deleted_msg.author.mention} deleted a message in {deleted_msg.channel.mention}',
                    description=f'`{deleted_msg.content}`',
                    color=self.config['embed']['color']['red']
                )

                delete_embed.set_thumbnail(url=deleted_msg.author.avatar)
                delete_embed.set_footer(text=self.config['embed']['footer'])

                # print(f'message deleted by {deleted_msg.author.name}')
                await log_channel.send(embed=delete_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):  # message log
        if self.config['module']['log']['message'] and self.config['module']['events']:
            if not before.author.id == self.client.user.id:
                if not before.content == after.content:

                    log_channel = self.client.get_channel(self.config['id']['log_channel'])

                    edit_embed = nextcord.Embed(
                        title=f'{before.author} made an edit',
                        description=f'Member {before.author.mention} edited a message in {before.channel.mention}\n[Jump to message]({after.jump_url})',
                        color=self.config['embed']['color']['yellow']
                    )

                    edit_embed.set_thumbnail(url=before.author.avatar)
                    edit_embed.add_field(name='Before:', value=f'`{before.content}`', inline=True)
                    edit_embed.add_field(name='After:', value=f'`{after.content}`', inline=True)
                    edit_embed.set_footer(text=self.config['embed']['footer'])

                    await log_channel.send(embed=edit_embed)
                    # print(f'Edit was made by {before.author.name}')

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):  # message log
        if self.config['module']['log']['message'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            bulk_embed = nextcord.Embed(
                title=messages.author,
                description=f'Deleted `{len(messages)}` messages in {messages.channel.mention}',
                color=self.config['embed']['color']['red']
            )
            bulk_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=bulk_embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, name):  # channel log
        if self.config['module']['log']['channel'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            channel_delete_embed = nextcord.Embed(
                title=f'Channel `{name}` got deleted',
                color=self.config['embed']['color']['red']
            )

            channel_delete_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=channel_delete_embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, name):  # channel log
        if self.config['module']['log']['channel'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            channel_create_embed = nextcord.Embed(
                title=f'Created channel `{name}`',
                color=self.config['embed']['color']['green']
            )

            channel_create_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=channel_create_embed)
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):  # role log
        if self.config['module']['log']['role'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            role_create_embed = nextcord.Embed(
                title=f'Role created: {role.name}',
                description=f'ID: `{role.id}`',
                color=self.config['embed']['color']['green']
            )

            role_create_embed.add_field(name='Color:', value=f'`{role.mention}`')
            role_create_embed.add_field(name='Hoisted:', value=role.hoist)
            role_create_embed.add_field(name='Mentionable:', value=role.mentionable)
            role_create_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=role_create_embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):  # role log
        if self.config['module']['log']['role'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            role_deleted_embed = nextcord.Embed(
                title=f'Role deleted: {role.name}',
                color=self.config['embed']['color']['red']
            )
            role_deleted_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=role_deleted_embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):  # member log
        if self.config['module']['log']['member'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            member_join_embed = nextcord.Embed(
                title=f'{member.name} Joined',
                description=f'Bot: {member.bot}',
                color=self.config['embed']['color']['green']
            )

            member_join_embed.set_thumbnail(url=member.avatar)
            member_join_embed.add_field(name='Created:', value=member.created_at)
            member_join_embed.add_field(name='ID:', value=member.id)
            member_join_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=member_join_embed)

        if self.config['module']['welcome'] and self.config['module']['events']:

            general = self.client.get_channel(self.config['id']['general'])
            welcome_channel = self.client.get_channel(self.config['id']['welcome_channel'])

            introduction_channel = self.client.get_channel(self.config['id']['introduction_channel'])
            react_roles_channel = self.client.get_channel(self.config['id']['react_roles_channel'])
            level_roles_channel = self.client.get_channel(self.config['id']['level_roles_channel'])

            welcome_embed = nextcord.Embed(
                description=f'Welcome {member.mention}!',
                color=self.config['embed']['color']['default']
            )

            await welcome_channel.send(embed=welcome_embed)
            # await general.send(content=f'Welcome to FallBurn {member.mention}!')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):  # member log
        if self.config['module']['log']['member'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            member_left_embed = nextcord.Embed(
                title=f'{member.name} left!',
                color=self.config['embed']['color']['red']
            )

            member_left_embed.set_thumbnail(url=member.avatar)
            member_left_embed.add_field(name='Roles:', value=member.roles.name)
            member_left_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=member_left_embed)
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):  # invite log
        if self.config['module']['log']['invite'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            invite_create_embed = nextcord.Embed(
                title=f'Invite created by {invite.inviter}',
                description=f'discord.gg/{invite.id}',
                color=self.config['embed']['color']['yellow']
            )

            invite_create_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=invite_create_embed)
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):  # invite log
        if self.config['module']['log']['invite'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            invite_delete_embed = nextcord.Embed(
                title=f'Invite deleted',
                description=f'discord.gg/{invite.id}',
                color=self.config['embed']['color']['red']
            )

            invite_delete_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=invite_delete_embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, _guild, user):  # mod log
        if self.config['module']['log']['mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            ban_embed = nextcord.Embed(
                title=f'{user.name} got banned!',
                color=self.config['embed']['color']['red']
            )

            ban_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=ban_embed)

    @commands.Cog.listener()
    async def on_member_unban(self, _guild, user):  # mod log
        if self.config['module']['log']['mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            unban_embed = nextcord.Embed(
                title=f'{user.name} got unbanned',
                color=self.config['embed']['color']['red']
            )

            await log_channel.send(embed=unban_embed)

    @commands.Cog.listener()
    async def on_auto_moderation_rule_create(self, rule):  # discord auto mod log
        if self.config['module']['log']['discord_auto_mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            rule_create_embed = nextcord.Embed(
                title='Auto Moderation Rule Created',
                description=f'Created by {rule.creator}',
                color=self.config['embed']['color']['green']
            )

            rule_create_embed(name='Name:', value=f'`{rule.name}`')
            rule_create_embed.add_field(name='Enabled:', value=rule.enabled)
            rule_create_embed.add_field(name='Trigger type:', value=f'`{rule.trigger_type}`', inline=True)
            rule_create_embed.add_field(name='Event type:', value=f'`{rule.event_type}`', inline=True)
            rule_create_embed.add_field(name='Exempt channels:', value=f'`{rule.exempt_channels}`', inline=False)
            rule_create_embed.add_field(name='Exempt roles:', value=f'`{rule.exempt_roles}`', inline=True)
            rule_create_embed.add_field(name='Actions:', value=f'`{rule.actions}`', inline=False)
            rule_create_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=rule_create_embed)

    @commands.Cog.listener()
    async def on_auto_moderation_rule_update(self, rule):  # discord auto mod log
        if self.config['module']['log']['discord_auto_mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            rule_update_embed = nextcord.Embed(
                title='Auto Moderation Rule Updated',
                description=f'Created by: {rule.creator}',
                color=self.config['embed']['color']['green']
            )

            rule_update_embed(name='Name:', value=f'`{rule.name}`')
            rule_update_embed.add_field(name='Enabled:', value=rule.enabled)
            rule_update_embed.add_field(name='Trigger type:', value=f'`{rule.trigger_type}`', inline=True)
            rule_update_embed.add_field(name='Event type:', value=f'`{rule.event_type}`', inline=True)
            rule_update_embed.add_field(name='Exempt channels:', value=f'`{rule.exempt_channels}`', inline=False)
            rule_update_embed.add_field(name='Exempt roles:', value=f'`{rule.exempt_roles}`', inline=True)
            rule_update_embed.add_field(name='Actions:', value=f'`{rule.actions}`', inline=False)
            rule_update_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=rule_update_embed)

    @commands.Cog.listener()
    async def on_auto_moderation_rule_delete(self, rule):  # discord auto mod log
        if self.config['module']['log']['discord_auto_mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            rule_delete_embed = nextcord.Embed(
                title='Auto Moderation Rule Deleted',
                description=f'name: `{rule.name}`',
                color=self.config['embed']['color']['red']
            )

            rule_delete_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=rule_delete_embed)

    @commands.Cog.listener()
    async def on_auto_moderation_rule_execution(self, rule_exec):  # discord auto mod log
        if self.config['module']['log']['discord_auto_mod'] and self.config['module']['events']:

            log_channel = self.client.get_channel(self.config['id']['log_channel'])

            rule_execution_embed = nextcord.Embed(
                title=f'Auto Moderation Triggered in: {rule_exec.channel.mention}',
                description=f'Rule triggered by: {rule_exec.member.mention}',
                color=self.config['embed']['color']['yellow']
            )

            rule_execution_embed.add_field(name='Full message:', value=f'`{rule_exec.content}`', inline=False)
            rule_execution_embed.add_field(name='Matched content:', value=f'`{rule_exec.matched_content}`', inline=True)
            rule_execution_embed.add_field(name='Matched keyword:', value=f'`{rule_exec.matched_keyword}`', inline=True)
            rule_execution_embed.set_footer(text=self.config['embed']['footer'])

            await log_channel.send(embed=rule_execution_embed)


def setup(client):
    client.add_cog(Events(client))
