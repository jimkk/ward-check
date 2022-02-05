from statistics import mean
import ward_db

def get_stats(user_id):
    # if user is not None:
        # stats = [value for _, value in user['stats'].items()]
        # control_wards = mean([x['controlWards'] for x in stats])
        # normal_wards = mean([x['normalWards'] for x in stats])
        # control_wards_per_minute = mean([x['controlWardsPerMinute'] for x in stats])
        # normal_wards_per_minute = mean([x['normalWardsPerMinute'] for x in stats])
    normal_wards = []
    control_wards = []
    normal_wards_per_minute = []
    control_wards_per_minute = []
    for game_id in ward_db.get_user_games(user_id):
        game = ward_db.get_game(game_id)
        game_duration = game['info']['gameDuration']
        participant_data = game['info']['participants'][ward_db.get_user_info(user_id)['puuid']]
        control_wards = participant_data['detectorWardsPlaced']
        control_wards.append(control_wards)
        control_wards_per_minute.append(control_wards / game_duration)
        normal_wards = participant_data['wardsPlaced'] - control_wards
        normal_wards.append(normal_wards)
        normal_wards_per_minute.append(normal_wards / game_duration)
        

    return {
        'controlWards': mean(control_wards),
        'normalWards': mean(normal_wards),
        'controlWardsPerMinute': mean(control_wards_per_minute),
        'normalWardsPerMinute': mean(normal_wards_per_minute)
    }