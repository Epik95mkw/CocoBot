import datetime
from discord.ext import commands, tasks

from components import functions as f


class ScheduledFunctions(commands.Cog):
    def __init__(self, _bot: commands.Bot):
        self.bot = _bot
        self.on_map_rotation.start()

    def cog_unload(self):
        self.on_map_rotation.cancel()

    @tasks.loop(time=[datetime.time(hour=t, second=30) for t in range(0, 24, 2)])
    async def on_map_rotation(self):
        guilds = list(self.bot.guilds)
        await f.update_maps(guilds)
        await f.check_new_patch(guilds)
        await f.update_gear(guilds)
