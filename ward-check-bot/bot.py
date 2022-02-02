import discord
import requests
from ward_db import ward_db
import ward_stats

from users import Users

with open('api.key', 'r') as api_file:
    api_key = api_file.readline()

client = discord.Client()
users = []

# api_url = 'http://localhost:5000'
api_url = 'http://10.0.0.137:12345'
# users = Users()
db = ward_db()

@client.event
async def on_message(message):
    if not message.content.startswith('wc!'):
        return
    command = message.content.split(' ')[0][3:]
    match command:
        case 'check':
            user = db.get_user_info(str(message.author.id))
            if user is not None:
                r = requests.get(api_url + '/getgames/' + user['league_name'])
                if not r.ok:
                    return
                data = r.json()
                last_game = data['data'][0]
                await message.channel.send(f'Vision Wards: {last_game["controlWards"]}\nNormal Wards: {last_game["normalWards"]}')
                for game in data['data']:
                    db.add_stats(message.author.id, game)
            else:
                await message.channel.send("I don't know you. (try 'adduser' first.)", reference=message, delete_after=20)
        case 'adduser':
            db.add_user(message.author.id, message.content[message.content.find(' ')+1:])
            print(users)
        case 'stats':
            data = ward_stats.get_stats(db.get_user_info(message.author.id))
            await message.channel.send(f'Your Averages:\nControl Wards: { data["controlWards"] }\nNormal Wards: { data["normalWards"] }\
                    \nControl Wards Per Minute: { round(data["controlWardsPerMinute"], 3) }\nNormal Wards Per Minute:{ round(data["normalWardsPerMinute"], 3) }')
        case 'clearusers':
            db.clear_users()
            await message.channel.send('Users Cleared.')


    print(command)


@client.event
async def on_ready():
    print(f'{client.user} has connected.')

client.run(api_key)



