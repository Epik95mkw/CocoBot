from dataclasses import dataclass
import requests

URL = 'https://en-americas-support.nintendo.com/app/answers/detail/a_id/59461/~/how-to-update-splatoon-3'


@dataclass
class PatchInfo:
    version: str
    text: str


def get() -> PatchInfo | None:
    """ Scrape patch notes page and return information on latest version """
    res = requests.get(URL)
    if not res.ok:
        print(f'Failed to fetch patch notes page (response code {res.status_code}: {res.reason})')
        return None
    html =  res.text

    updateline = None
    for i, line in enumerate(html.splitlines()):
        if 'Latest update:' in line:
            updateline = line
            break

    if updateline is None:
        return None

    s = updateline.find(':') + 2
    e = updateline.rfind('<')
    vtext = updateline[s:e]
    vnum = vtext.split(' ')[1]

    return PatchInfo(vnum, vtext)
