import datetime
import time
from typing import Iterable

import discord
from discord.ext import commands, tasks

from api import splatoon3ink, patchnotes
from core import embeds
from core.config import Config
from utils.paginator import Paginator

class ScheduledTasks(commands.Cog):
    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config
        self.on_map_rotation.start()
        self.on_check_patch.start()

    def cog_unload(self):
        self.on_map_rotation.cancel()
        self.on_check_patch.cancel()


    @tasks.loop(time=[datetime.time(hour=t, second=30) for t in range(0, 24, 2)])
    async def on_map_rotation(self):
        """ Runs 30 seconds after start of each rotation (to account for API delay) """
        await self.update_map_embeds(self.bot.guilds, self.config)
        await self.update_shop_embeds(self.bot.guilds, self.config)

    @tasks.loop(minutes=5)
    async def on_check_patch(self):
        """ Runs every 5 minutes """
        await self.check_new_patch(self.bot.guilds, self.config)


    @staticmethod
    async def update_map_embeds(guilds: Iterable[discord.Guild], config: Config):
        """ Update all map embeds in every server """
        data = splatoon3ink.get_map_data()
        if data is None:
            return

        embed_map = {
            'main': embeds.create_maps_embed(data),
            'sr': embeds.create_sr_embed(data),
            'challenge': embeds.create_challenge_embed(data),
            'eggstra': embeds.create_eggstra_embed(data)
        }

        for guild in guilds:
            for embed_key, embed_cfg in config[guild.id]['embeds']['schedules'].items():
                embed_content = embed_map[embed_key]
                if embed_cfg['ch_id'] is None:
                    # Guild has no target channel set for this embed, so skip
                    continue

                channel = guild.get_channel(embed_cfg['ch_id'])
                if channel is None:
                    # Target channel for this embed has been deleted, so skip
                    embed_cfg['ch_id'] = None
                    continue

                if embed_content is not None:
                    # Embed exists and content exists, so updated embed
                    pager = Paginator(embed_content)
                    try:
                        message = await channel.fetch_message(embed_cfg['msg_id'] or 0)
                        await pager.update_message(message)
                    except (discord.NotFound, discord.HTTPException):
                        # Message containing this embed does not exist, so send new one
                        await pager.send(channel)
                        message = pager.message
                    embed_cfg['msg_id'] = message.id

                elif embed_cfg['msg_id'] is not None:
                    # Embed exists but content does not exist, so delete embed
                    try:
                        message = await channel.fetch_message(embed_cfg['msg_id'])
                        await message.delete()
                    except (discord.NotFound, discord.HTTPException):
                        # Message containing this embed does not exist, so do nothing
                        pass
                    embed_cfg['msg_id'] = None

                time.sleep(0.1)  # Avoid rate limit

        config.save()

    @staticmethod
    async def update_shop_embeds(guilds: Iterable[discord.Guild], config: Config):
        """ Update all shop embeds in every server """
        data = splatoon3ink.get_shop_data()
        if data is None:
            return

        embed_content = embeds.create_shop_embed(data)
        embed = discord.Embed.from_dict(embed_content)

        for guild in guilds:
            embed_cfg = config[guild.id]['embeds']['gear']
            if not embed_cfg:
                continue
            channel = guild.get_channel(embed_cfg['ch_id'])
            if channel is None:
                embed_cfg['ch_id'] = None
                continue

            try:
                message = await channel.fetch_message(embed_cfg['msg_id'] or 0)
                await message.edit(embed=embed)
            except (discord.NotFound, discord.HTTPException):
                message = await channel.send(embed=embed)
                embed_cfg['msg_id'] = message.id

            time.sleep(0.1)

        config.save()

    @staticmethod
    async def check_new_patch(guilds: Iterable[discord.Guild], config: Config):
        """ Check if patch notes page has been updated. If so, send URL in patch notes channel """
        version_number, version_text = patchnotes.latest()
        if version_number is None:
            return

        for guild in guilds:
            patch_channel = config[guild.id]['channels']['patch']
            if not patch_channel:
                continue

            if config[guild.id]['latest_patch'] == version_number:
                # If latest version on patch notes page matches stored version, skip
                continue

            channel = guild.get_channel(patch_channel)
            if channel is None:
                continue

            content = (
                f'{guild.default_role} New patch notes: {version_text}\n'
                f'{patchnotes.URL}'
            )
            await channel.send(content)

            config[guild.id]['latest_patch'] = version_number
        config.save()
