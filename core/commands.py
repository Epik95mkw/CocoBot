import random

from discord.ext import commands
from discord.ext.commands import command

from api import weapondata, maplist
from core.config import Config


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config
        self.maplist = None


    @command(name='randomweapon', aliases=['rw'])
    async def random_weapon(self, ctx, *args: str):
        result = weapondata.get_random(*args)
        if result is None:
            await ctx.send('Failed to find weapon with this property')
        else:
            await ctx.send(result, reference=ctx.message, mention_author=False)


    @command(name='randommap', aliases=['rmap'])
    async def random_map(self, ctx, *args: str):
        args = [a.upper() for a in args]
        map_list = maplist.get()

        if map_list is None:
            await ctx.send('Error: Maplist not found')
            return
        elif 'ALL' in args:
            allowed_maps = map_list['legal'] + map_list['banned']
        else:
            allowed_maps = map_list['legal']

        while args:
            a = args.pop()
            if a in ('SZ', 'TC', 'RM', 'CB'):
                allowed_maps = [m for m in allowed_maps if m.startswith(a)]
                break
        choice = random.choice(allowed_maps)
        await ctx.send(choice, reference=ctx.message, mention_author=False)
