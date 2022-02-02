from flask import Flask
import requests
from match_db import match_db
app = Flask(__name__)

region_v4 = "na1"
region_v5 = "americas"
base_api_v4 = "https://" + region_v4 + ".api.riotgames.com"
base_api_v5 = "https://" + region_v5 + ".api.riotgames.com"

api_key = ""
with open('api.key', 'r') as api_key_file:
    api_key = api_key_file.readline()

db = match_db()

# ---------------- Endpoints ---------------- #
@app.route('/')
def root():
    return "Current supported routes:\n \
            getlastgame/<Summoner Name (case sensitive)>"

@app.route('/getgames/<summoner_name>')
def getgames(summoner_name):
    puuid = get_puuid(summoner_name)
    if puuid is None:
        return "Failed to get puuid"
    r = requests.get(base_api_v5 + '/lol/match/v5/matches/by-puuid/{}/ids'.format(puuid), headers={'X-Riot-Token': api_key})
    if not r.ok:
        return "Failed to get matches"
    games_ward_data = []
    match_list = r.json()
    for match_id in match_list:
        game_data = db.get_game(match_id)
        if game_data is None:
            print('Getting game from Riot API')
            match_response = requests.get(base_api_v5 + '/lol/match/v5/matches/{match_id}'.format(match_id = match_id), headers={'X-Riot-Token': api_key})
            if not match_response.ok:
                return "Failed to get match info. Match Id = {}".format(match_id)
            game_data = match_response.json()
            db.add_game(game_data)
        if game_data['info']['gameMode'] == 'CLASSIC':
            participants = game_data['info']['participants']
            summoner_info = [x for x in participants if x['puuid'] == puuid][0]
            control_wards = summoner_info['detectorWardsPlaced']
            normal_wards = summoner_info['wardsPlaced'] - control_wards
            games_ward_data.append({
                'match_id': match_id,
                'duration': game_data['info']['gameDuration'],
                'normalWards': normal_wards,
                'controlWards': control_wards
            })
    return {'data': games_ward_data}
    
@app.route('/setapikey/<new_api_key>')
def set_api_key(new_api_key):
    api_key = new_api_key
    return 'Success'

# ---------------- Utility ---------------- #
def get_puuid(summoner_name):
    r = requests.get(base_api_v4 + "/lol/summoner/v4/summoners/by-name/" + summoner_name, headers={'X-Riot-Token': api_key})
    if not r.ok:
        return None
    data = r.json()
    return data['puuid']
