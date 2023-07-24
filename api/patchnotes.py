import requests

URL = 'https://en-americas-support.nintendo.com/app/answers/detail/a_id/59461/~/how-to-update-splatoon-3'


def get():
    """ Get HTML from patch notes page """
    res = requests.get(URL)
    if not res.ok:
        print(f'Failed to fetch data (response code {res.status_code}: {res.reason})')
        return False
    return res.text


def latest():
    html = get()
    if not html:
        return None, None

    updateline = ''
    for i, line in enumerate(html.splitlines()):
        if '<section class="update-versions">' in line:
            updateline = html.splitlines()[i+1].strip()
            break

    if not updateline:
        return None, None

    s = len('<h3><a name=\"')
    e = len(updateline) - len('</a></h3>')
    vnum = updateline[s:s+4]
    vtext = updateline[s+6:e]
    return vnum, vtext
