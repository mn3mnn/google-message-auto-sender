# send post requests to test the api

import requests
import json
from dotenv import load_dotenv
from os import getenv
import json
import threading

load_dotenv()

send_url = f'http://localhost:3000{getenv("SEND_MSG_API")}'


# send 10 async requests
for i in range(50, 55):
    msg = {
        "message": f"test message{i}",
        "number": "201122960525",
        "key": getenv("API_KEY"),
        "type": "sms",
        "devices": "device1",
        "prioritize": 1
    }
    # threading.Thread(target=requests.post, args=(send_url, msg)).start()
    response = requests.post(send_url, json=msg)
    print(response.text)


