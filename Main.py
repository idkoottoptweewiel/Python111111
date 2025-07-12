import os, json, sys, time
from datetime import datetime

for lib in ['requests', 'websockets']:
    try:__import__(lib)
    except:os.system(f'pip install {lib}')

import requests
from websockets.sync.client import connect

Webhook = input('Webhook URL: ')

os.system('cls')

try:
    with connect('wss://api.rbxgold.com/socket.io/?EIO=4&transport=websocket', user_agent_header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36') as websocket:
        
        Rain_Happening = False

        websocket.recv()
        websocket.send('40')
        websocket.recv()
        websocket.recv()
        websocket.send('42["rain-join"]')
        websocket.recv()

        while True:
            response = websocket.recv()
            if response == '2':
                websocket.send('3')
            elif '42["rain-stream"' in response:
                try:
                    response = response.removeprefix('42["rain-stream",').removesuffix(']')
                    json_response = json.loads(response)['documents'][0]
                    Status = json_response['status']
                    Amount = round(json_response['evAmount'] + json_response['tipAmount'])
                    if Rain_Happening:
                        if Status == 'pending':
                            Rain_Happening = False
                            print('\n\nRain Ended\n')
                            data = {'content' : f'Rain Ended <t:{int(time.mktime(datetime.now().timetuple()))}:R>.', 'username' : 'RBXGold Rain Notifier', 'avatar_url': 'https://i.imgur.com/WKs4WTp.png'}
                            result = requests.post(Webhook, json = data)
                        else:
                            sys.stdout.write(f'\rAmount: {Amount}' + ' '*100)
                            sys.stdout.flush()
                    else:
                        if Status == 'in progress':
                            Rain_Happening = True
                            data = {'content' : f'@everyone Rain Started <t:{int(time.mktime(datetime.now().timetuple()))}:R>.', 'username' : 'RBXGold Rain Notifier', 'avatar_url': 'https://i.imgur.com/WKs4WTp.png'}
                            result = requests.post(Webhook, json = data)
                except:
                    pass

except Exception as oops:
    print(oops)
