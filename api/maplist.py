import os
import json
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()
path = os.path.join(os.path.dirname(__file__), f'..{os.getenv('MAPLISTPATH')}')

_cache = {}

class MapList(TypedDict):
    legal: list[str]
    banned: list[str]

def reload():
    if os.path.isfile(path):
        with open(path, 'r') as f:
            _cache['maplist'] = json.load(f)

def get() -> MapList | None:
    return _cache.get('maplist', None)

reload()
