import discord
from discord.ext.commands import command
from discord.ext.commands.core import Command

from components.functions import requires_perms, debug_msg
from api import mapdata, patchnotes, shopdata, weapondata
from components.config import config, Mode
from utils.dotdict import DotDict


@command(name='help')
@requires_perms(owner=False)
async def help_command(ctx):
    """ List available commands """
    await ctx.send(embed=discord.Embed.from_dict({
        'title': 'Commands',
        'fields': [{
            'name': '',
            'value': '\n'.join([v.name for v in globals().values() if isinstance(v, Command)])
        }]
    }))


@command(name='randomweapon', aliases=['rw'])
async def random_weapon(ctx, *args: str):
    result = weapondata.get_random(args)
    if result is None:
        await ctx.send('Failed to find weapon with this property')
    else:
        await ctx.send(result, reference=ctx.message, mention_author=False)


@command(name='set-debug-channel')
@requires_perms(owner=False)
async def set_debug_channel(ctx):
    """ Set channel for bot errors and debug info """
    config[ctx.guild.id].channels.debug = ctx.channel.id
    if config.update():
        await debug_msg(ctx, f'Set debug channel to {ctx.channel.jump_url}')
    else:
        await debug_msg(ctx, f'Failed to set debug channel to {ctx.channel.jump_url}')


@command(name='set-announcements')
@requires_perms(owner=False)
async def set_announcements(ctx):
    """ Set channel for announcement messages """
    config[ctx.guild.id].channels.announce = ctx.channel.id
    if config.update():
        await debug_msg(ctx, f'Set announcements channel to {ctx.channel.jump_url}')
    else:
        await debug_msg(ctx, f'Failed to set announcements channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='add-react-role')
@requires_perms(owner=False)
async def add_react_role(ctx, emoji: str, *_):
    """ Set replied message to give role when reacted to with emoji """
    target = await _get_react_msg(ctx)
    if target is None:
        return
    roles = ctx.message.role_mentions
    await target.add_reaction(emoji)
    for role in roles:
        config[ctx.guild.id].reactions += [DotDict({
            "msg_id": target.id,
            "emoji": emoji,
            "role_id": role.id
        })]
    if config.update():
        await debug_msg(ctx, f'React roles {[r.name for r in roles]} set to {target.jump_url}')
    else:
        await debug_msg(ctx, f'Failed to add react role.')
    await ctx.message.delete()


@command(name='set-maps-channel')
@requires_perms(owner=False)
async def set_maps_channel(ctx):
    """ Set map rotation embed to this channel """
    await _set_embed_channel(ctx, Mode.MAIN, pager=mapdata.get_main_maps(mapdata.get()))
    await debug_msg(ctx, f'Set map schedule channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='set-sr-channel')
@requires_perms(owner=False)
async def set_sr_channel(ctx):
    """ Set salmon run rotation embeds to this channel """
    data = mapdata.get()
    await _set_embed_channel(ctx, Mode.SR, pager=mapdata.get_sr_shifts(data))
    await _set_embed_channel(ctx, Mode.EGGSTRA, pager=mapdata.get_eggstra_shifts(data))
    await debug_msg(ctx, f'Set salmon run schedule channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='set-challenge-channel')
@requires_perms(owner=False)
async def set_challenge_channel(ctx):
    """ Set challenge schedule embed to this channel """
    await _set_embed_channel(ctx, Mode.CHALLENGE, pager=mapdata.get_challenges(mapdata.get()))
    await debug_msg(ctx, f'Set salmon run schedule channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='set-gear-channel')
@requires_perms(owner=False)
async def set_gear_channel(ctx):
    """ Set challenge schedule embed to this channel """
    embed = discord.Embed.from_dict(shopdata.formatted(shopdata.get()))
    await _set_embed_channel(ctx, 'gear', embed=embed)
    await debug_msg(ctx, f'Set splatnet gear channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='set-patch-channel')
@requires_perms(owner=False)
async def set_patch_channel(ctx):
    """ Set patch notes announcements to this channel """
    config[ctx.guild.id].channels.patch = DotDict({
        "ch_id": ctx.channel.id,
        "last": patchnotes.latest()[0]
    })
    config.update()
    await debug_msg(ctx, f'Set patch notes channel to {ctx.channel.jump_url}')
    await ctx.message.delete()


@command(name='set-anarchy-role')
@requires_perms(owner=False)
async def set_anarchy_role(ctx, _):
    roles = ctx.message.role_mentions
    if roles:
        config[ctx.guild.id].roles.maps = roles[0].id
        config.update()
        await debug_msg(ctx, f'Set anarchy notif role to {roles[0].name}')
    else:
        await debug_msg(ctx, 'No roles specified')


@command(name='set-sr-role')
@requires_perms(owner=False)
async def set_sr_role(ctx, _):
    roles = ctx.message.role_mentions
    if roles:
        config[ctx.guild.id].roles.sr = roles[0].id
        config.update()
        await debug_msg(ctx, f'Set salmon run notif role to {roles[0].name}')
    else:
        await debug_msg(ctx, 'No roles specified')


@command(name='splatfest')
@requires_perms(owner=False)
async def splatfest_setup(ctx, team1, color1, team2, color2, team3, color3):
    # 1. Generate new roles
    # 2. Add roles to config to be deleted after fest
    # 3. Send react role message in current channel
    pass


@command(name='give-perms')
@requires_perms(owner=True)
async def give_perms(ctx):
    """ Only server owner can use. Gives command permissions to any pinged roles. """
    roles = ctx.message.role_mentions
    if not roles:
        await debug_msg(ctx, 'No roles specified')
        return

    new_perms = list(set(config[ctx.guild.id].perms) | {r.id for r in roles})  # remove duplicates
    if config[ctx.guild.id].perms == new_perms:
        await debug_msg(ctx, 'Permissions already exist')
    else:
        config[ctx.guild.id].perms = new_perms
        config.update()
        await debug_msg(ctx, f'Allowed command usage for roles {[r.name for r in roles]}')


@command(name='remove-perms')
@requires_perms(owner=True)
async def remove_perms(ctx):
    """ Only server owner can use. Removes permissions for any pinged roles. """
    roles = ctx.message.role_mentions
    if not roles:
        await debug_msg(ctx, 'No roles specified')
        return

    new_perms = list(set(config[ctx.guild.id].perms) - {r.id for r in roles})
    if config[ctx.guild.id].perms == new_perms:
        await debug_msg(ctx, 'No permissions exist')
    else:
        config[ctx.guild.id].perms = new_perms
        config.update()
        await debug_msg(ctx, f'Removed command usage from roles {[r.name for r in roles]}')


@command(name='reset-server')
@requires_perms(owner=True)
async def reset_server(ctx, server_id=None):
    """ Only server owner can use. Removes all server data from bot. """
    if server_id != str(ctx.guild.id):
        await ctx.send('Provide server ID to confirm.')
        return
    config.delete(ctx.guild.id)
    if config.update():
        await ctx.send('Removed all server data from bot.')
    else:
        await ctx.send('Failed to remove server data.')


# HELPERS #


async def _set_embed_channel(ctx, key, *, embed=None, pager=None):
    if embed is not None:
        message = await ctx.send(embed=embed)
        msg_id = message.id
    elif pager is not None:
        await pager.send(ctx)
        msg_id = pager.message.id
    else:
        msg_id = 0

    if prev := config[ctx.guild.id].embeds[key]:
        prevmsg = await ctx.guild.get_channel(prev.ch_id).fetch_message(prev.msg_id)
        await prevmsg.delete()

    config[ctx.guild.id].embeds[key] = DotDict({
        "ch_id": ctx.channel.id,
        "msg_id": msg_id
    })
    config.update()


async def _get_react_msg(ctx):
    error_msg = ''
    if ctx.message.reference is None:
        error_msg = 'Target message not found (command must be reply)'
    if not error_msg and not ctx.message.role_mentions:
        error_msg = 'Role not specified'
    if error_msg:
        await debug_msg(ctx, f'{ctx.message.jump_url}\n{error_msg}')
        return None
    return await ctx.message.channel.fetch_message(ctx.message.reference.message_id)


async def setup(bot):
    for x in globals().values():
        if isinstance(x, Command):
            bot.add_command(x)
