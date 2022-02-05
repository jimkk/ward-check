from email.errors import MessageError
import discord
import requests
from ward_db import ward_db
import ward_stats
import os
import ward_api

from users import Users

with open('api.key', 'r') as api_file:
    api_key = api_file.readline()

client = discord.Client()



db = ward_db()
# print(api_url)

@client.event
async def on_message(message):
    if not message.content.startswith('wc!'):
        return
    command = message.content.split(' ')[0][3:]
    match command:
        case 'check':
            user = db.get_user_info(str(message.author.id))
            if user is not None:
                print("Getting data for: " + user['league_name'])
                # r = requests.get(api_url + '/getgames/' + user['league_name'])
                # if not r.ok:
                #     return
                # data = r.json()
                data = ward_api.get_games(user)
                last_game = data['data'][0]
                await message.channel.send(f'Vision Wards: {last_game["controlWards"]}\nNormal Wards: {last_game["normalWards"]}')
                for game in data['data']:
                    db.add_stats(message.author.id, game)
            else:
                await message.channel.send("I don't know you. (try 'adduser' first.)", reference=message, delete_after=20)
        case 'adduser':
            user_id = message.author.id
            league_name = message.content[message.content.find(' ')+1:]
            user_puuid = ward_api.get_id(league_name)
            db.add_user(user_id, league_name, user_puuid)
        case 'stats':
            async with message.channel.typing():
                data = db.get_stats(message.author.id)
                await message.channel.send(f'Your Averages:\nControl Wards: { round(data["controlWards"],3) }\nNormal Wards: { round(data["normalWards"],3) }\
                        \nControl Wards Per Minute: { round(data["controlWardsPerMinute"], 3) }\nNormal Wards Per Minute:{ round(data["normalWardsPerMinute"], 3) }')

        case 'test':
            print(db.get_user_games(message.author.id))

        case 'clearusers':
            db.clear_users()
            await message.channel.send('Users Cleared.')


    print(command)


@client.event
async def on_ready():
    print(f'{client.user} has connected.')

client.run(api_key)



