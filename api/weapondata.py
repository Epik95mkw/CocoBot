import random
import re
import requests


URL = 'https://splatoonwiki.org/wiki/List_of_weapons_in_Splatoon_3'


def get():
    res = requests.get(URL)
    if not res.ok:
        print(f'Failed to fetch wiki html (response code {res.status_code}: {res.reason})')
        return False
    return res.text


def scrape_wiki_page():
    html = get()
    tabledata = []
    headerdata = []
    table = html.replace('\n', '').partition('<tbody')[2].partition('</tbody>')[0]
    rows = table.split('</tr><tr')
    headers = rows.pop(0).split('</th>')[1:-1]

    def remove_html_tags(s: str) -> str:
        return re.sub(r'(<[^>]*>)|(&#.*?;)', '', s).strip()

    for header in headers:
        headerdata.append(remove_html_tags(header))

    for row in rows:
        rowdata = {}
        entries = row.split('</td>')[1:-1]

        for i, entry in enumerate(entries):
            rowdata[headerdata[i]] = remove_html_tags(entry)

        tabledata.append(rowdata)

    return tabledata


data = globals().setdefault('data', scrape_wiki_page())


def get_random(args: tuple[str]):
    if not args:
        weapons = [w['Main'] for w in data]
    else:
        filter_by = ' '.join(list(args)).lower()
        weapons = [w['Main'] for w in data if filter_by in [v.lower() for v in w.values()]]
        if not weapons:
            return None

    return random.choice(weapons)
