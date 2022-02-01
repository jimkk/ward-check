import numpy as np

class Users:
    users = [{'id': '161603549917216768', 'name': 'TyrannicalTRex', 'stats': []}] # for testing
    
    def in_users(self, user):
        for u in self.users:
            if u['id'] == str(user):
                return u
        return None

    def add(self, id, name):
        if self.in_users(id) is None:
            self.users.append({
                'id': str(id),
                'name': name,
                'stats': []
            })

    def add_stats(self, id, stats):
        user = self.in_users(id)
        if user is not None:
            stats = [x for x in stats if x['match_id'] not in [x['match_id'] for x in user['stats']]]
            for stat in stats:
                print(stat['match_id'])
                stat['controlWardsPerMinute'] = stat['controlWards'] / (stat['duration'] / 60)
                stat['normalWardsPerMinute'] = stat['normalWards'] / (stat['duration'] / 60)
            user['stats'] = user['stats'] + stats


    def get_stats(self, id):
        user = self.in_users(id)
        if user is not None:
            control_wards = np.average([x['controlWards'] for x in user['stats']])
            normal_wards = np.average([x['normalWards'] for x in user['stats']])
            control_wards_per_minute = np.average([x['controlWardsPerMinute'] for x in user['stats']])
            normal_wards_per_minute = np.average([x['normalWardsPerMinute'] for x in user['stats']])
            return {
                'controlWards': control_wards,
                'normalWards': normal_wards,
                'controlWardsPerMinute': control_wards_per_minute,
                'normalWardsPerMinute': normal_wards_per_minute
            }


    def __str__(self):
        return str(self.users)