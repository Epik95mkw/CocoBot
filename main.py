import os
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

from core.commands import Commands
from core.listeners import Listeners
from core.scheduled import ScheduledFunctions
from core.config import config
from core import functions as f

load_dotenv()
TOKEN = os.getenv('TOKEN')
CONFIGPATH = os.getenv('CONFIGPATH')

bot = commands.Bot(
    command_prefix='\\',
    intents=discord.Intents.all(),
    help_command=None
)


@bot.event
async def on_ready():
    guilds = list(bot.guilds)
    config.load(CONFIGPATH, guilds)

    await bot.add_cog(Commands(bot))
    await bot.add_cog(Listeners(bot))
    await bot.add_cog(ScheduledFunctions(bot))

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


# DEBUG COMMANDS


@bot.command(name='get-config')
@commands.is_owner()
async def get_config(ctx):
    """ Only bot owner can use. Send config.json file for debugging. """
    await ctx.send(file=discord.File(config.path))


@bot.command(name='set-config')
@commands.is_owner()
async def set_config(ctx):
    """ Only bot owner can use. Overwrite config.json with given file. """
    if not ctx.message.attachments:
        await ctx.send('Missing attachment')
        return
    await ctx.send(content='Old config:', file=discord.File(config.path))
    await ctx.message.attachments[0].save(fp=config.path)
    config.load(CONFIGPATH)
    await ctx.send('Successfully updated config')


if __name__ == '__main__':
    bot.run(TOKEN)
