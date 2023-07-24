from discord.ext.commands import Cog
from components.config import config


class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, ev):
        roles, member = _get_react_roles(self.bot, ev)
        if roles and member != self.bot.user:
            new_roles = [r for r in roles if r not in member.roles]
            await member.add_roles(*new_roles)

    @Cog.listener()
    async def on_raw_reaction_remove(self, ev):
        roles, member = _get_react_roles(self.bot, ev)
        if roles:
            had_roles = [r for r in roles if r in member.roles]
            await member.remove_roles(*had_roles)

    # TODO: debug message if react role deleted
    @Cog.listener()
    async def on_raw_message_delete(self, ev):
        updated = [x for x in config[ev.guild_id].reactions if x.msg_id == ev.message_id]
        if updated:
            config[ev.guild_id].reactions = updated
            config.update()


def _get_react_roles(bot, ev):
    valid_reactions = [
        x for x in config[ev.guild_id].reactions if
        x.msg_id == ev.message_id and x.emoji == str(ev.emoji)
    ]
    guild = bot.get_guild(ev.guild_id)
    member = guild.get_member(ev.user_id)
    return [guild.get_role(x.role_id) for x in valid_reactions], member
