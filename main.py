from messanger import *
from urls import *
# from api import *

import requests
import http
import datetime
import time


send_response_url = SEND_RESPONSE_URL


def main():
    messanger = Messanger()
    messanger.login()

    while True:

        messages = Message.get_messages_by_status('unsent')
        for message in messages:
            msg_id = message.id
            mobile_number = message.mobile_number
            message_content = message.content
            if not all([msg_id, mobile_number, message_content]):
                continue

            status = messanger.send_message(mobile_number, message_content)
            status_date = datetime.datetime.now()

            if status == 'failed':
                Message.set_msg_status(msg_id, status)
            elif status == 'sent':
                Message.set_msg_status(msg_id, status)
            elif status == 'timeout':
                Message.set_msg_status(msg_id, status)

            try:
                msg_json = {
                    'ID': msg_id,
                    'status': status,
                    'dst_number': mobile_number
                }
                print(requests.post(send_response_url, json=msg_json))

            except Exception as e:
                print('Error sending response to the user(client)')
                print(e)

        time.sleep(0.1)


        # response = requests.get(get_unsent_messages_url + f'&key={API_KEYS[0]}')
        # if response.status_code == 200:
        #     data = response.json()
        #     messages = data.get('data', {}).get('messages', [])
        #     for message in messages:
        #         msg_id = message.get('ID', None)
        #         mobile_number = message.get('number', None)
        #         message_content = message.get('message', None)
        #         if not all([msg_id, mobile_number, message_content]):
        #             continue
        #
        #         status = messanger.send_message(mobile_number, message_content)
        #         status_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #
        #         if status == 'failed':
        #             Message.update_msg_status(msg_id, status)  # update status in the database
        #         elif status == 'sent':
        #             Message.update_msg_status(msg_id, status)
        #         elif status == 'timeout':
        #             Message.update_msg_status(msg_id, status)
        #
        #         # send response to the user(client)
        #         requests.get(send_response_url.format(msg_id, status_date, status))
        #
        # time.sleep(5)


if __name__ == "__main__":
    main()
