import requests
import os

api_url = 'http://localhost:12345'
# api_url = 'http://10.0.0.137:12345'

env_url_name = 'WARD_CHECK_API_URL'
env_url = os.environ.get(env_url_name)
if env_url is not None:
    api_url = env_url
else:
    print(f'{env_url_name} was not found in the env variables. Defaulting to dev url')
print(api_url)

def get_id(summoner_name):
    r = requests.get(api_url + f'/id/{summoner_name}')
    if r.ok:
        return r.json()['puuid']

def get_games(user):
    r = requests.get(api_url + '/getgames/' + user['league_name'])
    if not r.ok:
        return
    data = r.json()
    return data