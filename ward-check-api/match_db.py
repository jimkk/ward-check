import os
import firebase_admin
from firebase_admin import credentials, db

class match_db:

    db_ref = None

    def __init__(self) -> None:
        cred_location = os.environ.get('FIREBASE_CRED')
        if cred_location is None:
            raise Exception('Missing $FIREBASE_CRED value.')

        cred = credentials.Certificate(cred_location)
        firebase_admin.initialize_app(cred,{
            'databaseURL': 'https://matchhistory-b7495.firebaseio.com/'
        })

    def add_game(self, game):
        db_ref = db.reference('/games/' + game['metadata']['matchId'])
        db_ref.set(game)

    def get_game(self, match_id):
        db_ref = db.reference('/games')
        for key, value in db_ref.get().items():
            if key == match_id:
                return value
        return None