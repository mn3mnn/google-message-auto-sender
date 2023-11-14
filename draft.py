import requests
send_response_url = SEND_RESPONSE_URL = 'http://192.155.107.231:5003/receive/statusircs'

try:
    msg_json = {
        'ID': 'msg_id',
        'status': 'status',
    }
    print(requests.get(send_response_url, json=msg_json))

except Exception as e:
    print('Error sending response to the user(client)')
    print(e)