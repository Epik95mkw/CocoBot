import datetime
import time
from typing import Iterable

import discord
from discord.ext import commands, tasks

from api import splatoon3ink, patchnotes
from core import embeds
from core.config import Mode, config
from utils.paginator import Paginator


class ScheduledTasks(commands.Cog):
    def __init__(self, _bot: commands.Bot):
        self.bot = _bot
        self.on_map_rotation.start()
        self.on_check_patch.start()

    def cog_unload(self):
        self.on_map_rotation.cancel()
        self.on_check_patch.cancel()


    @tasks.loop(time=[datetime.time(hour=t, second=30) for t in range(0, 24, 2)])
    async def on_map_rotation(self):
        """ Runs 30 seconds after start of each rotation (to account for API delay) """
        await self.update_map_embeds(self.bot.guilds)
        await self.update_shop_embeds(self.bot.guilds)

    @tasks.loop(minutes=5)
    async def on_check_patch(self):
        """ Runs every 5 minutes """
        await self.check_new_patch(self.bot.guilds)


    @staticmethod
    async def update_map_embeds(guilds: Iterable[discord.Guild]):
        data = splatoon3ink.get_map_data()
        if data is None:
            return

        embed_map = {
            Mode.MAIN: embeds.create_maps_embed(data),
            Mode.SR: embeds.create_sr_embed(data),
            Mode.CHALLENGE: embeds.create_challenge_embed(data),
            Mode.EGGSTRA: embeds.create_eggstra_embed(data)
        }

        for guild in guilds:
            for mode, embed_content in embed_map.items():
                embed_cfg = config[guild.id].embeds[mode]
                if not embed_cfg:
                    # Guild has no target channel set for this embed, so skip
                    continue

                channel = guild.get_channel(embed_cfg.ch_id)
                if channel is None:
                    # Target channel for this embed has been deleted, so skip
                    continue

                if embed_content is not None:
                    # Embed exists and content exists, so updated embed
                    pager = Paginator(embed_content)
                    try:
                        message = await channel.fetch_message(embed_cfg.msg_id)
                        await pager.update_message(message)
                    except (discord.NotFound, discord.HTTPException):
                        # Message containing this embed does not exist, so send new one
                        await pager.send(channel)
                        message = pager.message
                    config[guild.id].embeds[mode].msg_id = message.id

                elif embed_cfg.msg_id != 0:
                    # Embed exists but content does not exist, so delete embed
                    try:
                        message = await guild.get_channel(embed_cfg.ch_id).fetch_message(embed_cfg.msg_id)
                        await message.delete()
                    except (discord.NotFound, discord.HTTPException):
                        # Message containing this embed does not exist, so do nothing
                        pass
                    config[guild.id].embeds[mode].msg_id = 0

                time.sleep(0.1)  # Avoid rate limit

        config.update()

    @staticmethod
    async def update_shop_embeds(guilds: Iterable[discord.Guild]):
        data = splatoon3ink.get_shop_data()
        if data is None:
            return

        embed_content = embeds.create_shop_embed(data)
        embed = discord.Embed.from_dict(embed_content)

        for guild in guilds:
            embed_cfg = config[guild.id].embeds.gear
            if not embed_cfg:
                continue
            channel = guild.get_channel(embed_cfg.ch_id)
            if channel is None:
                continue

            try:
                message = await channel.fetch_message(embed_cfg.msg_id)
                await message.edit(embed=embed)
            except (discord.NotFound, discord.HTTPException):
                message = await channel.send(embed=embed)
                config[guild.id].embeds.gear.msg_id = message.id

            time.sleep(0.1)

        config.update()

    @staticmethod
    async def check_new_patch(guilds: Iterable[discord.Guild]):
        """ Check if patch notes page has been updated. If so, send URL in patch notes channel. """
        version_number, version_text = patchnotes.latest()
        if version_number is None:
            return

        for guild in guilds:
            patch_cfg = config[guild.id].channels.patch
            if not patch_cfg:
                continue

            if patch_cfg.last == version_number:
                # If latest version on patch notes page matches stored version, skip
                continue

            channel = guild.get_channel(patch_cfg.ch_id)
            if channel is None:
                continue

            content = (
                f'{guild.default_role} New patch notes: {version_text}\n'
                f'{patchnotes.URL}'
            )
            await channel.send(content)

            config[guild.id].channels.patch.last = version_number
        config.update()
