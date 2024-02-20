from flask.cli import with_appcontext

from messanger import Messanger

from api import *

import requests
from threading import Thread
from subprocess import Popen
import http
import datetime
import time
import sys
import logging
from constants import SENT, FAILED, TIMEOUT, TIMEOUT_WAITING, MAKE_SMS_CHAT_FAILED

send_response_url = SEND_RESPONSE_URL


# Configure logging
log_file_path = 'messages_status.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')


def send_response_to_client(msg_id, status, mobile_number):
    msg_json = {
        'ID': msg_id,
        'status': status,
        'dst_number': mobile_number
    }

    try:
        logging.info(f'\nSending response: {msg_json}\n')
    except:
        pass

    try:
        res = requests.post(send_response_url, json=msg_json)
        print(res)
    except Exception as e:
        print(e)


def worker():
    global STOP
    print("Worker started")

    messanger = Messanger()
    messanger.set_timeout_waiting(TIMEOUT_WAITING)
    messanger.set_make_sms_chat_failed(MAKE_SMS_CHAT_FAILED)
    messanger.login()

    while not STOP:
        messages = Message.get_messages_by_status('unsent')
        for message in messages:
            try:
                msg_id = message.id
                mobile_number = message.mobile_number
                message_content = message.content
                if not all([msg_id, mobile_number, message_content]):
                    continue
                print(f"whitelisted numbers: {WHITELISTED_NUMBERS}")
                print(f"non whitelisted numbers response: {WHITELISTED_NUMBERS_RESPONSE[0]}")
                print(f"mobile number: {mobile_number}")
                if mobile_number not in WHITELISTED_NUMBERS:
                    print(f"Number {mobile_number} not in whitelist")
                    Message.set_msg_status(msg_id, WHITELISTED_NUMBERS_RESPONSE[0])
                    print(f"Message status set to {WHITELISTED_NUMBERS_RESPONSE[0]}")
                    send_response_to_client(msg_id, WHITELISTED_NUMBERS_RESPONSE[0], mobile_number)
                    print(f"Response sent to client")
                    continue

                status = messanger.send_message(mobile_number, message_content)
                # status_date = datetime.datetime.utcnow()

                if status == FAILED:
                    Message.set_msg_status(msg_id, status)
                elif status == SENT:
                    Message.set_msg_status(msg_id, status)
                elif status == TIMEOUT:
                    Message.set_msg_status(msg_id, status)

                send_response_to_client(msg_id, status, mobile_number)

            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    STOP = False

    worker_thread = Thread(target=worker)
    worker_thread.start()

    app.run(debug=True, use_reloader=False)  # port=5000

