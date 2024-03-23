import discord
from time import sleep

from api import mapdata, patchnotes, shopdata
from core.config import config
from utils.paginator import Paginator


async def debug_msg(guild: discord.Guild, content: str):
    """ Send message in debug channel if specified, otherwise send through ctx. """
    if config and (debug := config[guild.id].channels.debug):
        debug_ch = guild.get_channel(debug)
        await debug_ch.send(content)
    elif guild.system_channel is not None:
        await guild.system_channel.send(content)


async def announcement(guild, role_key, content):
    """ Send message in announcement channel if specified. """
    ch_id = config[guild.id].channels.announcements
    if not ch_id:
        return

    ping = ''
    if role_key:
        role_id = config[guild.id].roles[role_key]
        if role_id:
            ping = guild.get_role(role_id).mention
    else:
        ping = guild.default_role

    await guild.get_channel(ch_id).send(f'{ping} {content}' if ping else content)


async def update_maps(guilds: list[discord.Guild]):
    """ Fetch from map API and update all map embeds. """
    data = mapdata.get()
    if not data:
        return

    embeds = mapdata.format_all(data)

    for guild in guilds:
        for mode, info in embeds.items():
            if not info.pages:
                await delete_map_embed(guild, mode)
                sleep(0.1)
                continue

            if (a := info.announcement) is not None:
                await announcement(guild, a.role_key, a.message)

            await update_map_embed(guild, mode, info.pages)
            sleep(0.1)

    config.update()


async def update_map_embed(guild, mode: str, new_embed: list[dict]):
    """ Update a single map embed in a given guild. """
    cfg = config[guild.id].embeds[mode]
    if not cfg:  # No channel set for this guild
        return

    channel = guild.get_channel(cfg.ch_id)
    pager = Paginator(new_embed)

    try:
        message = await channel.fetch_message(cfg.msg_id)
        await pager.update_message(message)
    except (discord.NotFound, discord.HTTPException):
        await pager.send(channel)
        message = pager.message
    config[guild.id].embeds[mode].msg_id = message.id


async def delete_map_embed(guild, mode: str):
    """ Delete a temporary map embed in a given guild. """
    cfg = config[guild.id].embeds[mode]
    if not cfg or cfg.msg_id == 0:  # No channel set, or message already deleted
        return

    try:
        message = await guild.get_channel(cfg.ch_id).fetch_message(cfg.msg_id)
        await message.delete()
    except (discord.NotFound, discord.HTTPException):
        pass
    config[guild.id].embeds[mode].msg_id = 0


async def check_new_patch(guilds: list[discord.Guild]):
    """ Check if patch notes page has been updated. If so, send URL in patch notes channel. """
    vnum, vtext = patchnotes.latest()
    if vnum is None:
        return

    for guild in guilds:
        cfg = config[guild.id].channels.patch
        if not cfg:
            continue
        if cfg.last == vnum:
            continue

        channel = guild.get_channel(cfg.ch_id)
        content = f'{guild.default_role} New patch notes: {vtext}\n' \
                  f'{patchnotes.URL}'
        await channel.send(content)

        config[guild.id].channels.patch.last = vnum
    config.update()


async def update_gear(guilds: list[discord.Guild]):
    data = shopdata.get()
    if not data:
        return

    embed = discord.Embed.from_dict(shopdata.formatted(data))

    for guild in guilds:
        cfg = config[guild.id].embeds.gear
        if not cfg:
            continue
        channel = guild.get_channel(cfg.ch_id)

        try:
            message = await channel.fetch_message(cfg.msg_id)
            await message.edit(embed=embed)
        except (discord.NotFound, discord.HTTPException):
            message = await channel.send(embed=embed)
            config[guild.id].embeds.gear.msg_id = message.id
        sleep(0.1)

    config.update()
