# send post requests to test the api

import requests
from urls import *

from api import *

send_msg_url = f'http://localhost:' + str(API_PORT) + SEND_MSG_ROUTE


for i in range(5):
    data = {
        'key': API_KEYS[0],
        'message': f'Test message {i}',
        'number': '0912345678',
        'type': 'sms'
    }
    response = requests.post(send_msg_url, json=data)
    print(response.status_code)
    print(response.text)
    print()
