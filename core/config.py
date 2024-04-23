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
        """ Loads config from specified JSON file """
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
        """ Write current state to JSON file """
        as_dict = self.data  # {gid: gcfg.data for gid, gcfg in self.data}
        pretty = json.dumps(as_dict, indent=2)
        with open(self.path, 'w') as f:
            f.write(pretty)
        return True

    def delete(self, guild):
        """ Clear all data for specified guild """
        self.data[guild.id] = DotDict(TEMPLATE)


config = BotConfig()
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
