import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import command as slash_command

from api import patchnotes, weapondata, splatoon3ink
from core import embeds
from core.config import Config
from core.scheduled_tasks import ScheduledTasks
from utils.paginator import Paginator


@app_commands.guild_only()
@app_commands.default_permissions()
class AppCommands(commands.GroupCog, group_name='admin'):
    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config


    @slash_command(name='update-weapons')
    async def update_weapons(self, interaction):
        """ Update list of weapons for randomweapon command """
        newdata = weapondata.scrape_wiki_page()
        if weapondata.data != newdata:
            weapondata.data = newdata
            msg = 'Successfully updated weapon data'
        else:
            msg = 'No new data found'
        await interaction.response.send_message(msg, ephemeral=True)


    @slash_command(name='update-maps')
    async def update_maps(self, interaction):
        """ Manually update map and shop embeds """
        await ScheduledTasks.update_map_embeds(self.bot.guilds, self.config)
        await ScheduledTasks.update_shop_embeds(self.bot.guilds, self.config)
        await interaction.response.send_message('Updated map data', ephemeral=True)


    @slash_command(name='reset-maps')
    async def reset_maps(self, interaction):
        """ Force reset map and shop embeds """
        embed_config = self.config[interaction.guild.id]['embeds']
        for embed_config in [*embed_config['schedules'].values(), embed_config['gear']]:
            if embed_config is not None:
                embed_config['msg_id'] = None
        self.config.save()
        await ScheduledTasks.update_map_embeds(self.bot.guilds, self.config)
        await ScheduledTasks.update_shop_embeds(self.bot.guilds, self.config)
        await interaction.response.send_message('Reset map embeds', ephemeral=True)


    @slash_command(name='check-patch')
    async def check_patch(self, interaction):
        await ScheduledTasks.check_new_patch(self.bot.guilds, self.config)
        await interaction.response.send_message('Updated patch data', ephemeral=True)


    @slash_command(name='set-debug-channel')
    async def set_debug_channel(self, interaction):
        """ Set channel for bot errors and debug info """
        self.config[interaction.guild.id]['channels']['debug'] = interaction.channel.id
        msg = f'{"Set" if self.config.save() else "Failed to set"} debug channel to {interaction.channel.jump_url}'
        await interaction.response.send_message(msg, ephemeral=True)


    @slash_command(name='set-announcements')
    async def set_announcements(self, interaction):
        """ Set channel for announcement messages """
        self.config[interaction.guild.id]['channels']['announcements'] = interaction.channel.id
        msg = f'{"Set" if self.config.save() else "Failed to set"} announcements channel to {interaction.channel.jump_url}'
        await interaction.response.send_message(msg, ephemeral=True)


    @slash_command(name='add-react-role')
    async def add_react_role(self, interaction, message_id: str, emoji: str, role: discord.Role):
        """ Set replied message to give role when reacted to with emoji """
        async def send(msg):
            await interaction.response.send_message(msg, ephemeral=True)

        m_id = int(message_id.split('-')[-1])
        target = await interaction.channel.fetch_message(m_id)
        try:
            await target.add_reaction(emoji)
        except (TypeError, discord.NotFound):
            await send('Invalid emoji')
            return
        self.config[interaction.guild.id]['reactions'].append({
            "msg_id": target.id,
            "emoji": emoji,
            "role_id": role.id
        })
        if self.config.save():
            await send(f'React role {role.name} set to {target.jump_url}')
        else:
            await send('Failed to add react role.')


    @slash_command(name='set-maps-channel')
    async def set_maps_channel(self, interaction):
        """ Set map rotation embed to this channel """
        api_data = splatoon3ink.get_map_data()
        embed_content = embeds.create_maps_embed(api_data)
        embed_cfg = self.config[interaction.channel.guild.id]['embeds']['schedules']['main']
        await self._set_embed_channel(interaction.channel, embed_cfg, pagerinfo=embed_content)
        await interaction.response.send_message(
            f'Set map rotation embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-sr-channel')
    async def set_sr_channel(self, interaction):
        """ Set salmon run rotation embeds to this channel """
        api_data = splatoon3ink.get_map_data()
        embed_content = embeds.create_sr_embed(api_data)
        embed_cfg = self.config[interaction.channel.guild.id]['embeds']['schedules']['sr']
        await self._set_embed_channel(interaction.channel, embed_cfg, pagerinfo=embed_content)

        embed_content = embeds.create_eggstra_embed(api_data)
        embed_cfg = self.config[interaction.channel.guild.id]['embeds']['schedules']['eggstra']
        await self._set_embed_channel(interaction.channel, embed_cfg, pagerinfo=embed_content)

        await interaction.response.send_message(
            f'Set salmon run embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-challenge-channel')
    async def set_challenge_channel(self, interaction):
        """ Set challenge schedule embed to this channel """
        api_data = splatoon3ink.get_map_data()
        embed_content = embeds.create_challenge_embed(api_data)
        embed_cfg = self.config[interaction.channel.guild.id]['embeds']['schedules']['challenge']
        await self._set_embed_channel(interaction.channel, embed_cfg, pagerinfo=embed_content)
        await interaction.response.send_message(
            f'Set challenge embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-gear-channel')
    async def set_gear_channel(self, interaction):
        """ Set challenge schedule embed to this channel """
        api_data = splatoon3ink.get_shop_data()
        embed_content = discord.Embed.from_dict(embeds.create_shop_embed(api_data))
        embed_cfg = self.config[interaction.channel.guild.id]['embeds']['gear']
        await self._set_embed_channel(interaction.channel, embed_cfg, embed=embed_content)
        await interaction.response.send_message(
            f'Set gear embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-patch-channel')
    async def set_patch_channel(self, interaction):
        """ Set patch notes announcements to this channel """
        self.config[interaction.guild.id]['channels']['patch'] = interaction.channel.id
        patch_data = patchnotes.get()
        if patch_data is not None:
            self.config[interaction.guild.id]['latest_patch'] = patch_data.version
        self.config.save()
        await interaction.response.send_message(
            f'Set patch announcements channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-anarchy-role')
    async def set_anarchy_role(self, interaction, role: discord.Role):
        """ Set role to ping for anarchy announcements """
        self.config[interaction.guild.id]['roles']['main'] = role.id
        self.config.save()
        await interaction.response.send_message(
            f'Set anarchy notif role to {role.name}',
            ephemeral=True
        )

    @slash_command(name='set-sr-role')
    async def set_sr_role(self, interaction, role: discord.Role):
        """ Set role to ping for salmon run announcements """
        self.config[interaction.guild.id]['roles']['sr'] = role.id
        self.config.save()
        await interaction.response.send_message(
            f'Set salmon run notif role to {role.name}',
            ephemeral=True
        )

    @slash_command(name='reset-server')
    async def reset_server(self, interaction, server_id: str):
        """ Removes all data for this server from bot. """
        async def send(msg):
            await interaction.response.send_message(msg, ephemeral=True)
        if server_id != str(interaction.guild.id):
            await send('Provide server ID to confirm.')
            return
        self.config.clear_guild(interaction.guild.id)
        if self.config.save():
            await send('Removed all server data from bot.')
        else:
            await send('Failed to remove server data.')

    # HELPERS #

    async def _set_embed_channel(self, channel, embed_cfg, *, embed=None, pagerinfo=None):
        if embed is not None:
            message = await channel.send(embed=embed)
            msg_id = message.id
        elif pagerinfo is not None:
            pager = Paginator(pagerinfo)
            await pager.send(channel)
            msg_id = pager.message.id
        else:
            msg_id = None

        if embed_cfg['ch_id'] is not None:
            try:
                prev_channel = channel.guild.get_channel(embed_cfg['ch_id'])
                if prev_channel is not None:
                    prev_message = await prev_channel.fetch_message(embed_cfg['msg_id'])
                    await prev_message.delete()
            except discord.NotFound:
                pass

        embed_cfg.update({
            "ch_id": channel.id,
            "msg_id": msg_id
        })
        self.config.save()
