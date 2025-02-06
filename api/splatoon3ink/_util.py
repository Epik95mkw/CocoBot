import requests

BASE_URL = 'https://splatoon3.ink/data'

def fetch_api(endpoint: str):
    """ Get JSON response from splatoon3.ink API """
    res = requests.get(BASE_URL + endpoint)
    if not res.ok:
        print(f'Failed to fetch splatoon3.ink data (response code {res.status_code}: {res.reason})')
        return None
    return res.json()['data']
