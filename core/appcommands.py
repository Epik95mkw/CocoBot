import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import command as slash_command

from api import mapdata, patchnotes, shopdata, weapondata
from core.config import config, Mode
from core.scheduled_tasks import ScheduledTasks
from utils.dotdict import DotDict
from utils.paginator import Paginator


@app_commands.guilds(*config.guild_ids)
@app_commands.guild_only()
@app_commands.default_permissions()
class AppCommands(commands.GroupCog, group_name='admin'):
    def __init__(self, _bot: commands.Bot):
        self.bot = _bot


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
        await ScheduledTasks.update_map_embeds(self.bot.guilds)
        await ScheduledTasks.update_map_embeds(self.bot.guilds)
        await interaction.response.send_message('Updated map data', ephemeral=True)


    @slash_command(name='reset-maps')
    async def reset_maps(self, interaction):
        """ Force reset map and shop embeds """
        for embed_name in config[interaction.guild.id].embeds:
            config[interaction.guild.id].embeds[embed_name].msg_id = ''
        config.update()
        await ScheduledTasks.update_map_embeds(self.bot.guilds)
        await ScheduledTasks.update_map_embeds(self.bot.guilds)
        await interaction.response.send_message('Reset map embeds', ephemeral=True)


    @slash_command(name='set-debug-channel')
    async def set_debug_channel(self, interaction):
        """ Set channel for bot errors and debug info """
        config[interaction.guild.id].channels.debug = interaction.channel.id
        msg = f'{"Set" if config.update() else "Failed to set"} debug channel to {interaction.channel.jump_url}'
        await interaction.response.send_message(msg, ephemeral=True)


    @slash_command(name='set-announcements')
    async def set_announcements(self, interaction):
        """ Set channel for announcement messages """
        config[interaction.guild.id].channels.announce = interaction.channel.id
        msg = f'{"Set" if config.update() else "Failed to set"} announcements channel to {interaction.channel.jump_url}'
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
        config[interaction.guild.id].reactions += [DotDict({
            "msg_id": target.id,
            "emoji": emoji,
            "role_id": role.id
        })]
        if config.update():
            await send(f'React role {role.name} set to {target.jump_url}')
        else:
            await send('Failed to add react role.')


    @slash_command(name='set-maps-channel')
    async def set_maps_channel(self, interaction):
        """ Set map rotation embed to this channel """
        await _set_embed_channel(interaction.channel, Mode.MAIN, pagerinfo=mapdata.get_main_maps(mapdata.get()))
        await interaction.response.send_message(
            f'Set map rotation embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-sr-channel')
    async def set_sr_channel(self, interaction):
        """ Set salmon run rotation embeds to this channel """
        data = mapdata.get()
        await _set_embed_channel(interaction.channel, Mode.SR, pagerinfo=mapdata.get_sr_shifts(data))
        await _set_embed_channel(interaction.channel, Mode.EGGSTRA, pagerinfo=mapdata.get_eggstra_shifts(data))
        await interaction.response.send_message(
            f'Set salmon run embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-challenge-channel')
    async def set_challenge_channel(self, interaction):
        """ Set challenge schedule embed to this channel """
        await _set_embed_channel(interaction.channel, Mode.CHALLENGE, pagerinfo=mapdata.get_challenges(mapdata.get()))
        await interaction.response.send_message(
            f'Set challenge embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-gear-channel')
    async def set_gear_channel(self, interaction):
        """ Set challenge schedule embed to this channel """
        embed = discord.Embed.from_dict(shopdata.formatted(shopdata.get()))
        await _set_embed_channel(interaction.channel, 'gear', embed=embed)
        await interaction.response.send_message(
            f'Set gear embed channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-patch-channel')
    async def set_patch_channel(self, interaction):
        """ Set patch notes announcements to this channel """
        config[interaction.guild.id].channels.patch = DotDict({
            "ch_id": interaction.channel.id,
            "last": patchnotes.latest()[0]
        })
        config.update()
        await interaction.response.send_message(
            f'Set patch announcements channel to {interaction.channel.jump_url}',
            ephemeral=True
        )


    @slash_command(name='set-anarchy-role')
    async def set_anarchy_role(self, interaction, role: discord.Role):
        """ Set role to ping for anarchy announcements """
        config[interaction.guild.id].roles.maps = role.id
        config.update()
        await interaction.response.send_message(
            f'Set anarchy notif role to {role.name}',
            ephemeral=True
        )

    @slash_command(name='set-sr-role')
    async def set_sr_role(self, interaction, role: discord.Role):
        """ Set role to ping for salmon run announcements """
        config[interaction.guild.id].roles.sr = role.id
        config.update()
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
        config.delete(interaction.guild.id)
        if config.update():
            await send('Removed all server data from bot.')
        else:
            await send('Failed to remove server data.')


# HELPERS #

async def _set_embed_channel(channel, key, *, embed=None, pagerinfo=None):
    if embed is not None:
        message = await channel.send(embed=embed)
        msg_id = message.id
    elif pagerinfo is not None and pagerinfo.pages:
        pager = Paginator(pagerinfo.pages)
        await pager.send(channel)
        msg_id = pager.message.id
    else:
        msg_id = 0

    if prev := config[channel.guild.id].embeds[key]:
        try:
            prevmsg = await channel.guild.get_channel(prev.ch_id).fetch_message(prev.msg_id)
            await prevmsg.delete()
        except discord.NotFound:
            pass

    config[channel.guild.id].embeds[key] = DotDict({
        "ch_id": channel.id,
        "msg_id": msg_id
    })
    config.update()
