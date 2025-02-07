import os
import json
from enum import Enum
from io import TextIOWrapper
from typing import Optional, TypedDict

from discord.ext import commands


# class Mode(Enum):
#     """ Pseudo-enum that contains constants for each of the 4 gamemode types. """
#     MAIN = 'main'
#     SR = 'sr'
#     CHALLENGE = 'challenge'
#     EGGSTRA = 'eggstra'


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


TEMPLATE: GuildConfig = {
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

    def __repr__(self):
        return str(self._config)

    def __getitem__(self, guild_id: int) -> GuildConfig:
        return self._config[guild_id]

    def save(self):
        with open(self.path, 'w') as f:  # type: TextIOWrapper[str]
            json.dump(self._config, f, indent=2)
        return True

    def load(self):
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
            self._config.setdefault(guild.id, TEMPLATE)

        self.save()

    def clear_guild(self, guild_id: int):
        """ Clear all data for specified guild """
        self._config[guild_id] = TEMPLATE





# class BotConfig:
#     path: str
#     data = {}  # shared by all instances
#     loaded = False
#
#     def load(self, path: str, guilds=()):
#         """ Loads config from specified JSON file """
#         self.path = os.path.join(os.path.dirname(__file__),  f'..{path}')
#
#         if not os.path.isfile(self.path):
#             open(self.path, 'x').close()
#         else:
#             with open(self.path, 'r') as f:
#                 configjson = json.load(f)
#             for k, v in configjson.items():
#                 self.data[int(k)] = DotDict(v)
#
#         for guild in guilds:
#             self.data.setdefault(guild.id, DotDict(TEMPLATE))
#
#         self.update()
#         self.loaded = True
#
#     def __bool__(self):
#         return self.loaded
#
#     def __getitem__(self, key: int):
#         return self.data[key]
#
#     @property
#     def guild_ids(self) -> list[int]:
#         return list(self.data.keys())
#
#     def update(self):
#         """ Write current state to JSON file """
#         as_dict = self.data  # {gid: gcfg.data for gid, gcfg in self.data}
#         pretty = json.dumps(as_dict, indent=2)
#         with open(self.path, 'w') as f:
#             f.write(pretty)
#         return True
#
#     def delete(self, guild):
#         """ Clear all data for specified guild """
#         self.data[guild.id] = DotDict(TEMPLATE)


"""
{ (GUILD ID): Template }\n
Template:\n
perms: [ role IDs ]\n
roles: { main, sr, events } (role ID)\n
channels: {\n
. . debug, announcement, patch: { ch_id, last: str }\n
} (channel ID)\n
embeds: {\n
. . main, sr, challenge, eggstra, gear\n
} ({ ch_id, msg_id })\n
reactions: [{ msg_id, emoji, role_id }]\n
"""
