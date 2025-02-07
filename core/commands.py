from discord.ext import commands
from discord.ext.commands import command

from api import weapondata
from core.config import Config


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config

    @command(name='randomweapon', aliases=['rw'])
    async def random_weapon(self, ctx, *args: str):
        result = weapondata.get_random(*args)
        if result is None:
            await ctx.send('Failed to find weapon with this property')
        else:
            await ctx.send(result, reference=ctx.message, mention_author=False)
