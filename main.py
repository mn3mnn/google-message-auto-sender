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
    unsent_messages = Message.get_unsent_messages()
    if len(unsent_messages) > 3:
        unsent_messages = unsent_messages[:3]

    for msg in unsent_messages:
        mobile_number = msg.mobile_number
        content = msg.content
        msg_id = msg.id
        print(f"Sending message: {content} to {mobile_number}")
        try:
            bot.send_message(mobile_number, content)
            Message.update(status="pending", pending_at=datetime.datetime.utcnow()).where(Message.id == msg_id).execute()
            status = bot.get_msg_status()
            if status == "sent":
                Message.update(status="sent", sent_at=datetime.datetime.utcnow()).where(Message.id == msg_id).execute()

            elif status == "failed":
                Message.update(status="failed").where(Message.id == msg_id).execute()

            elif status == "timeout":
                Message.update(status="timeout").where(Message.id == msg_id).execute()

        except Exception as e:
            print(e)
            Message.update(status="failed").where(Message.id == msg_id).execute()

        time.sleep(1)

    time.sleep(5)


if __name__ == "__main__":
    main()
