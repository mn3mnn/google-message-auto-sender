import requests
import json
from constants import FAILED, TIMEOUT, SENT


# url = f'http://185.182.184.191'
url = f'http://127.0.0.1:5000'


white_list_numbers = ['2011xxxxxxx', '2010xxxxxxx']

white_list_response = FAILED



for num in white_list_numbers:
    data = {
        'number': num
    }
    response = requests.post(url + '/whitelist', json=data)
    print(response.json())


data = {
    'whitelist_response': white_list_response
}
response = requests.post(url + '/whitelist-response', json=data)
print(response.json())

