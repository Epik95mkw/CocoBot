import os
import json
from typing import List

from utils.dotdict import DotDict


class Mode:
    """ Pseudo-enum that contains constants for each of the 4 gamemode types. """
    MAIN = 'main'
    SR = 'sr'
    CHALLENGE = 'challenge'
    EGGSTRA = 'eggstra'


TEMPLATE = {
    "perms": [],
    "roles": {
        Mode.MAIN: "",
        Mode.SR: "",
        "events": "",
    },
    "channels": {
        "debug": "",
        "announcements": "",
        "patch": "",
    },
    "embeds": {
        Mode.MAIN: "",
        Mode.SR: "",
        Mode.CHALLENGE: "",
        Mode.EGGSTRA: "",
        "gear": "",
    },
    "reactions": [],
}


class BotConfig:
    path: str
    data = {}  # shared by all instances
    loaded = False

    def load(self, path: str, guilds=()):
        self.path = os.path.join(os.path.dirname(__file__),  f'..{path}')

        if not os.path.isfile(self.path):
            open(self.path, 'x').close()
        else:
            with open(self.path, 'r') as f:
                configjson = json.load(f)
            for k, v in configjson.items():
                self.data[int(k)] = DotDict(v)

        for guild in guilds:
            self.data.setdefault(guild.id, DotDict(TEMPLATE))

        self.update()
        self.loaded = True

    def __bool__(self):
        return self.loaded

    def __getitem__(self, key: int):
        return self.data[key]

    @property
    def guild_ids(self) -> List[int]:
        return list(self.data.keys())

    def update(self):
        as_dict = self.data  # {gid: gcfg.data for gid, gcfg in self.data}
        pretty = json.dumps(as_dict, indent=2)
        with open(self.path, 'w') as f:
            f.write(pretty)
        return True

    def delete(self, guild):
        self.data[guild.id] = DotDict(TEMPLATE)


config = BotConfig()


'''
Implement this later?
'''
# class GuildConfig:
#
#     def __init__(self, guild: discord.Guild, guild_data: dict):
#         self.guild = guild
#         self.data = guild_data
#
#     @property
#     def debug_channel(self):
#         ch_id = self.data['channels']['debug'] or 0
#         return self.guild.get_channel(ch_id)
#
#     @property
#     def announcements_channel(self):
#         ch_id = self.data['channels']['announcements'] or 0
#         return self.guild.get_channel(ch_id)
#
#     @property
#     def patch_channel(self):
#         patch_info = self.data['channels']['patch']
#         ch_id = 0 if not patch_info else patch_info['ch_id']
#         return self.guild.get_channel(ch_id)
#
#     def get_embed_channel(self, embed_key):
#         return self._get_embed_info(embed_key, 'ch_id')
#
#     def get_embed_message(self, embed_key):
#         return self._get_embed_info(embed_key, 'msg_id')
#
#     def _get_embed_info(self, embed_key, info_key):
#         embeds = self.data['embeds']
#         if embed_key not in embeds:
#             raise KeyError('Invalid embed type given (use constants in BotConfig)')
#         if not embeds[embed_key]:
#             return None
#         else:
#             return self.guild.get_channel(embeds[embed_key][info_key])
#
#     def set_embed_info(self, mode: str, channel: discord.TextChannel, message: discord.Message):
#         pass
