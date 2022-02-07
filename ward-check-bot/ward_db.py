import firebase_admin
from firebase_admin import credentials, db
from statistics import mean
import os

class ward_db:

    db_ref = None

    def __init__(self) -> None:
        cred_location = os.environ.get('FIREBASE_CRED')
        if cred_location is None:
            raise Exception('Missing $FIREBASE_CRED value.')

        cred = credentials.Certificate(cred_location)
        firebase_admin.initialize_app(cred,{
            'databaseURL': 'https://matchhistory-b7495.firebaseio.com/'
        })

    def add_user(self, user_id, name, puuid):
        db_ref = db.reference('/users')
        db_ref.push({
            'discord_id': str(user_id),
            'league_name': name,
            'puuid': puuid,
            'stats': [{}]
        })
    
    def get_user(self, user_id):
        db_ref = db.reference('/users')
        for key, value in db_ref.get().items():
            if value['discord_id'] == str(user_id):
                return (key, value)
        return None
        
    def get_user_info(self, user_id):
        user = self.get_user(user_id)
        if user is not None:
            return user[1]
        else:
            return None

    def get_user_key(self, user_id):
        user = self.get_user(user_id)
        if user is not None:
            return user[0]
        else:
            return None

    def add_stats(self, user_id, stats):
        user = self.get_user(user_id)
        if user is None:
            return
        db_ref = db.reference(f'/users/{user[0]}/stats')
        stats['controlWardsPerMinute'] = stats['controlWards'] / (stats['duration'] / 60)
        stats['normalWardsPerMinute'] = stats['normalWards'] / (stats['duration'] / 60)
        db_ref.push(stats)

    def get_stats(self, user_id):
        # if user is not None:
            # stats = [value for _, value in user['stats'].items()]
            # control_wards = mean([x['controlWards'] for x in stats])
            # normal_wards = mean([x['normalWards'] for x in stats])
            # control_wards_per_minute = mean([x['controlWardsPerMinute'] for x in stats])
            # normal_wards_per_minute = mean([x['normalWardsPerMinute'] for x in stats])
        normal_wards_list = []
        control_wards_list = []
        normal_wards_per_minute_list = []
        control_wards_per_minute_list = []
        for game_id in self.get_user_games(user_id):
            game = self.get_game(game_id)
            game_duration_minutes = game['info']['gameDuration'] / 60
            participants = game['info']['participants']
            participant_puuid = self.get_user_info(user_id)['puuid']
            participant_data = [x for x in participants if x['puuid'] == participant_puuid][0]
            control_wards = participant_data['detectorWardsPlaced']
            control_wards_list.append(control_wards)
            control_wards_per_minute_list.append(control_wards / game_duration_minutes)
            normal_wards = participant_data['wardsPlaced'] - control_wards
            normal_wards_list.append(normal_wards)
            normal_wards_per_minute_list.append(normal_wards / game_duration_minutes)
            

        return {
            'controlWards': mean(control_wards_list),
            'normalWards': mean(normal_wards_list),
            'controlWardsPerMinute': mean(control_wards_per_minute_list),
            'normalWardsPerMinute': mean(normal_wards_per_minute_list)
        }
    
    def get_game(self, game_id):
        db_ref = db.reference(f'/games/{game_id}')
        return db_ref.get()

    
    def get_user_games(self, user_id):
        puuid = self.get_user_info(user_id)['puuid']
        # print(puuid)
        db_ref = db.reference('/games')
        game_list=[]
        for match_id, game_data in db_ref.get().items():
            # print(game_data['metadata']['participants'])
            if puuid in game_data['metadata']['participants']:
                game_list.append(game_data['metadata']['matchId'])
        return game_list

    
            

    def clear_users(self):
        db_ref = db.reference('/users')
        db_ref.set({})