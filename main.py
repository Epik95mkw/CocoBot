import os
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

from components.listeners import Listeners
from components.scheduled import ScheduledFunctions
from components.config import config
from components import functions as f

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(
    command_prefix='\\',
    intents=discord.Intents.all(),
    help_command=None
)


@bot.event
async def on_ready():
    config.load(bot)
    await bot.load_extension('components.commands')
    await bot.add_cog(Listeners(bot))
    await bot.add_cog(ScheduledFunctions(bot))

    guilds = list(bot.guilds)
    await f.update_maps(guilds)
    await f.check_new_patch(guilds)
    await f.update_gear(guilds)

    print(f'Connected: {datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    await f.debug_msg(ctx, f'{ctx.message.jump_url}\n{error}')
    raise error.original


if __name__ == '__main__':
    bot.run(TOKEN)
