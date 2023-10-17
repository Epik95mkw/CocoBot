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
        if 'Latest update:' in line:
            updateline = line
            break

    if not updateline:
        return None, None

    s = updateline.find(':') + 2
    e = updateline.rfind('<')
    vtext = updateline[s:e]
    vnum = vtext.split(' ')[1]

    return vnum, vtext
