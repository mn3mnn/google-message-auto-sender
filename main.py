from db import *
from bot import *

import datetime
import time
import threading
import random


def main():
    bot = Bot()
    bot.login()

    # Todo: start updater thread

    # while True:
    count = 0
    unsent_messages = Message.get_unsent_messages()
    for msg in unsent_messages:
        if count == 2:
            break
        mobile_number = msg.mobile_number
        content = msg.content
        msg_id = msg.id
        print(f"Sending message: {content} to {mobile_number}")
        try:
            bot.send_message(mobile_number, content)
            Message.update(status="pending", pending_at=datetime.datetime.utcnow()).where(Message.id == msg_id).execute()

        except Exception as e:
            print(e)
            Message.update(status="failed").where(Message.id == msg_id).execute()

        time.sleep(2)

    # time.sleep(10)


if __name__ == "__main__":
    main()
