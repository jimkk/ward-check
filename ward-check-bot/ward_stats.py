from statistics import mean

def get_stats(user):
    if user is not None:
        stats = [value for _, value in user['stats'].items()]
        control_wards = mean([x['controlWards'] for x in stats])
        normal_wards = mean([x['normalWards'] for x in stats])
        control_wards_per_minute = mean([x['controlWardsPerMinute'] for x in stats])
        normal_wards_per_minute = mean([x['normalWardsPerMinute'] for x in stats])
        return {
            'controlWards': control_wards,
            'normalWards': normal_wards,
            'controlWardsPerMinute': control_wards_per_minute,
            'normalWardsPerMinute': normal_wards_per_minute
        }