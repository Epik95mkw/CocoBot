import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from core.commands import Commands
from core.appcommands import AppCommands
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
    await bot.add_cog(AppCommands(bot))
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
    await ctx.interaction.response.send_message(f'{error}', ephemeral=True)
    raise error


# DEBUG COMMANDS

@bot.command(name='sync')
@commands.is_owner()
async def sync_app_commands(ctx: commands.Context):
    """ Only bot owner can use. Syncs application commands. """
    msg = await ctx.reply('Syncing...')
    synced = await bot.tree.sync()
    await msg.edit(content=f'Synced {len(synced)} app commands.')


@bot.command(name='get-config')
@commands.is_owner()
async def get_config(ctx: commands.Context):
    """ Only bot owner can use. Send config.json file for debugging. """
    await ctx.send(file=discord.File(config.path))


@bot.command(name='set-config')
@commands.is_owner()
async def set_config(ctx: commands.Context):
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
