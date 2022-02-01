import math
import discord
import requests

from users import Users

with open('api.key', 'r') as api_file:
    api_key = api_file.readline()

client = discord.Client()
users = []

api_url = 'http://10.0.0.137:12345'
users = Users()

@client.event
async def on_message(message):
    if not message.content.startswith('wc!'):
        return
    command = message.content.split(' ')[0][3:]
    match command:
        case 'check':
            user = users.in_users(str(message.author.id))
            if user is not None:
                r = requests.get(api_url + '/getgames/' + user['name'])
                if not r.ok:
                    return
                data = r.json()
                last_game = data['data'][0]
                await message.channel.send(f'Vision Wards: {last_game["controlWards"]}\nNormal Wards: {last_game["controlWards"]}')
                users.add_stats(message.author.id, data['data'])
            else:
                await message.channel.send("I don't know you. (try 'adduser' first.)", reference=message, delete_after=20)
        case 'adduser':
            users.add(message.author.id, message.content[message.content.find(' ')+1:])
            print(users)
        case 'stats':
            data = users.get_stats(message.author.id)
            await message.channel.send(f'Your Averages:\nControl Wards: { data["controlWards"] }\nNormal Wards: { data["normalWards"] }\
                    \nControl Wards Per Minute: { round(data["controlWardsPerMinute"], 3) }\nNormal Wards Per Minute:{ round(data["normalWardsPerMinute"], 3) }')


    print(command)


@client.event
async def on_ready():
    print(f'{client.user} has connected.')

client.run(api_key)



