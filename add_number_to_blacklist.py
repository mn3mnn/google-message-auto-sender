import requests
import json
from constants import FAILED, TIMEOUT, SENT


url = f'http://185.182.184.191'
# url = f'http://127.0.0.1:5000'


black_list_numbers = ['201122960525']

black_list_response = FAILED





for num in black_list_numbers:
    data = {
        'number': num
    }
    response = requests.post(url + '/blacklist', json=data)
    print(response.json())


data = {
    'blacklist_response': black_list_response
}
response = requests.post(url + '/blacklist-response', json=data)
print(response.json())

