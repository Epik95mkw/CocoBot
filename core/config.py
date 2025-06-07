import os
import json
from io import TextIOWrapper
from typing import Optional, TypedDict

from discord.ext import commands


class ConfigRoles(TypedDict):
    """ Contains role IDs to ping for announcements """
    main:   Optional[int]
    sr:     Optional[int]
    events: Optional[int]

class ConfigChannels(TypedDict):
    """ Contains channel IDs to send automated announcements/messages to """
    debug:          Optional[int]
    announcements:  Optional[int]
    patch:          Optional[int]

class ConfigEmbed(TypedDict):
    """ Contains data for a single auto-updating embed """
    ch_id:  Optional[int]
    msg_id: Optional[int]

class ConfigMapEmbeds(TypedDict):
    """ Contains data for each type of auto-updating embed """
    main:       ConfigEmbed
    sr:         ConfigEmbed
    challenge:  ConfigEmbed
    eggstra:    ConfigEmbed

class ConfigEmbeds(TypedDict):
    """ Contains data for each type of auto-updating embed """
    schedules:  ConfigMapEmbeds
    gear:       ConfigEmbed

class ConfigReaction(TypedDict):
    """ Contains data for a react-role message """
    msg_id: int
    emoji: str
    role_id: int

class GuildConfig(TypedDict):
    """ Contains configuration for a particular server """
    perms:        list[int]
    roles:        ConfigRoles
    channels:     ConfigChannels
    embeds:       ConfigEmbeds
    reactions:    list[ConfigReaction]
    latest_patch: Optional[str]


GUILD_TEMPLATE: GuildConfig = {
    "perms": [],
    "roles": {
        "main": None,
        "sr": None,
        "events": None,
    },
    "channels": {
        "debug": None,
        "announcements": None,
        "patch": None,
    },
    "embeds": {
        "schedules": {
            "main":      {"ch_id": None, "msg_id": None},
            "sr":        {"ch_id": None, "msg_id": None},
            "challenge": {"ch_id": None, "msg_id": None},
            "eggstra":   {"ch_id": None, "msg_id": None},
        },
        "gear":      {"ch_id": None, "msg_id": None},
    },
    "reactions": [],
    "latest_patch": None,
}


class Config:
    def __init__(self, path: str, bot: commands.Bot):
        self.path = os.path.join(os.path.dirname(__file__), f'..{path}')
        self._bot = bot
        self._config = {}
        self._loaded = False

    def _assert_loaded(self):
        if not self._loaded:
            raise NotImplementedError(
                'Config must be initialized using `load()` before calling this function'
            )

    def __repr__(self):
        return str(self._config)

    def __getitem__(self, guild_id: int) -> GuildConfig:
        """ Get server-specific config by guild ID """
        self._assert_loaded()
        return self._config[guild_id]

    def save(self):
        """ Save current config state to JSON file """
        self._assert_loaded()
        with open(self.path, 'w') as f:  # type: TextIOWrapper[str]
            json.dump(self._config, f, indent=2)
        return True

    def load(self):
        """ Load config state stored in JSON file """
        if not os.path.isfile(self.path):
            # If config file doesn't exist, create it
            open(self.path, 'x').close()
        else:
            # If config file does exist, load data from it
            with open(self.path, 'r') as f:
                configjson = json.load(f)
            for k, v in configjson.items():
                self._config[int(k)] = v

        # Create GuildConfigs for any servers missing from config file
        for guild in self._bot.guilds:
            self._config.setdefault(guild.id, GUILD_TEMPLATE)

        self._loaded = True
        self.save()

    def clear_guild(self, guild_id: int):
        """ Clear all data for specified guild """
        self._assert_loaded()
        self._config[guild_id] = GUILD_TEMPLATE
