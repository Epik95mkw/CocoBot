from discord.ext.commands import Bot, Cog
from discord import RawReactionActionEvent, RawMessageDeleteEvent
from core.config import Config


class EventListeners(Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    @Cog.listener()
    async def on_raw_reaction_add(self, event: RawReactionActionEvent):
        roles, member = self._get_react_roles(event)
        if roles and member != self.bot.user:
            new_roles = [r for r in roles if r not in member.roles]
            await member.add_roles(*new_roles)

    @Cog.listener()
    async def on_raw_reaction_remove(self, event: RawReactionActionEvent):
        roles, member = self._get_react_roles(event)
        if roles:
            had_roles = [r for r in roles if r in member.roles]
            await member.remove_roles(*had_roles)

    # TODO: debug message if react role deleted
    @Cog.listener()
    async def on_raw_message_delete(self, event: RawMessageDeleteEvent):
        reactions = self.config[event.guild_id]['reactions']
        updated = [entry for entry in reactions if entry['msg_id'] != event.message_id]
        if updated != reactions:
            self.config[event.guild_id]['reactions'] = updated
            self.config.save()


    def _get_react_roles(self, event: RawReactionActionEvent):
        valid_reactions = [
            entry for entry in self.config[event.guild_id]['reactions'] if
            entry['msg_id'] == event.message_id and entry['emoji'] == str(event.emoji)
        ]
        guild = self.bot.get_guild(event.guild_id)
        member = guild.get_member(event.user_id)
        return [guild.get_role(entry['role_id']) for entry in valid_reactions], member
