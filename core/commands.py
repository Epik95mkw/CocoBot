import random

from discord.ext import commands
from discord.ext.commands import command

from api import weapondata, maplist
from core.config import Config


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config
        self.rmap_memory = []


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
        filter_by = []
        allow_banned = False
        no_repeats = False

        while args:
            a = args.pop()
            if a in ('SZ', 'TC', 'RM', 'CB'):
                filter_by.append(a)
            elif a == 'ALL':
                allow_banned = True
            elif a == 'NO-REPEAT':
                no_repeats = True
            elif a == 'RESET':
                no_repeats = False
                self.rmap_memory.clear()

        map_list = maplist.get()
        if map_list is None:
            await ctx.send('Error: Maplist not found', reference=ctx.message, mention_author=False)
            return
        else:
            allowed_maps = map_list['legal']

        if allow_banned:
            allowed_maps += map_list['banned']
        if filter_by:
            allowed_maps = [m for m in allowed_maps if m[0:2] in filter_by]
        if no_repeats or self.rmap_memory:
            allowed_maps = [m for m in allowed_maps if m not in self.rmap_memory]

        if not allowed_maps:
            await ctx.send('No more maps available!', reference=ctx.message, mention_author=False)
            return

        choice = random.choice(allowed_maps)
        message = choice
        if no_repeats or self.rmap_memory:
            self.rmap_memory.append(choice)
            message += '\n-# no-repeat: ON'
        await ctx.send(message, reference=ctx.message, mention_author=False)
