import datetime
from discord.ext import commands, tasks

from components import functions as f


class ScheduledFunctions(commands.Cog):
    def __init__(self, _bot: commands.Bot):
        self.bot = _bot
        self.on_map_rotation.start()
        self.check_patch.start()

    def cog_unload(self):
        self.on_map_rotation.cancel()
        self.check_patch.cancel()

    @tasks.loop(time=[datetime.time(hour=t, second=30) for t in range(0, 24, 2)])
    async def on_map_rotation(self):
        await f.update_maps(list(self.bot.guilds))
        await f.update_gear(list(self.bot.guilds))

    @tasks.loop(time=[datetime.time(hour=t, minute=m, second=30) for m in range(0, 60, 5) for t in range(0, 24, 1)])
    async def check_patch(self):
        await f.check_new_patch(list(self.bot.guilds))
