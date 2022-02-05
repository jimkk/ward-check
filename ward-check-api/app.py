from flask import Flask
import requests
from match_db import match_db
app = Flask(__name__)


regions = {
    4: "na1",
    5: "americas"
}

base_apis = {
    4:"https://" + regions[4] + ".api.riotgames.com",
    5:"https://" + regions[5] + ".api.riotgames.com"
}

api_key = ""
with open('api.key', 'r') as api_key_file:
    api_key = api_key_file.readline()

db = match_db()

# ---------------- Endpoints ---------------- #
@app.route('/')
def root():
    return "Current supported routes:\n \
            getlastgame/<Summoner Name (case sensitive)>"

@app.route('/getgames/<summoner_name>/<option>')
def getgames(summoner_name, option):
    puuid = get_puuid(summoner_name)
    if puuid is None:
        return f"Failed to get puuid for summoner name: {summoner_name}"
    match_list = get_riot_request('/lol/match/v5/matches/by-puuid/{}/ids'.format(puuid), version=5)
    return_data = []
    for match_id in match_list:
        game_data = db.get_game(match_id)
        if game_data is None:
            print('Getting game from Riot API')
            game_data = get_riot_request('/lol/match/v5/matches/{match_id}'.format(match_id = match_id), version=5)
            db.add_game(game_data)
        if option == 'wards':
            if game_data['info']['gameMode'] == 'CLASSIC':
                participants = game_data['info']['participants']
                summoner_info = [x for x in participants if x['puuid'] == puuid][0]
                control_wards = summoner_info['detectorWardsPlaced']
                normal_wards = summoner_info['wardsPlaced'] - control_wards
                return_data.append({
                    'match_id': match_id,
                    'duration': game_data['info']['gameDuration'],
                    'normalWards': normal_wards,
                    'controlWards': control_wards
                })
        else:
            return_data.append(game_data)
    return {'data': return_data}
    
@app.route('/id/<summoner_name>')
def get_id(summoner_name):
    return {
        'puuid': get_puuid(summoner_name)
    }

# ---------------- Utility ---------------- #
def get_puuid(summoner_name):
    data = get_riot_request(f'/lol/summoner/v4/summoners/by-name/{summoner_name}', version=4)
    if data is not None:
        return data['puuid']

def get_riot_request(endpoint, version = 4):
    url = base_apis[version] + endpoint
    r = requests.get(url, headers={'X-Riot-Token': api_key})
    if r.ok:
        return r.json()
    if r.status_code == 403:
        print('Invalid API Key')
    elif r.status_code == 404:
        print('Not Found')
    return None
