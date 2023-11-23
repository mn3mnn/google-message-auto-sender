# send post requests to test the api

import requests
from urls import *

from api import *

send_msg_url = f'http://185.182.184.191' + SEND_MSG_ROUTE
# send_msg_url = f'http://127.0.0.1:5000' + SEND_MSG_ROUTE


for i in range(3):
    data = {
        'key': API_KEYS[0],
        'message': f'teeeessssttt {i+1}',
        'number': '0912345678',
        'type': 'sms'
    }
    response = requests.post(send_msg_url, json=data)
    print(response.status_code)
    print(response.text)
    print()
