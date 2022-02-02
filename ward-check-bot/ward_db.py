import firebase_admin
from firebase_admin import credentials, db

class ward_db:

    db_ref = None

    def __init__(self) -> None:
        cred = credentials.Certificate("firebase.key")
        firebase_admin.initialize_app(cred,{
            'databaseURL': 'https://matchhistory-b7495.firebaseio.com/'
        })

    def add_user(self, user_id, name):
        db_ref = db.reference('/users')
        db_ref.push({
            'discord_id': str(user_id),
            'league_name': name,
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

    def clear_users(self):
        db_ref = db.reference('/users')
        db_ref.set({})