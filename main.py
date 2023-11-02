from messanger import *

import datetime
import time


def main():
    messanger = Messanger()
    messanger.login()

    # Todo: start updater thread

    while True:
        unsent_messages = Message.get_unsent_messages()

        for msg in unsent_messages:
            mobile_number = msg.mobile_number
            content = msg.content
            msg_id = msg.id
            print(f"Sending message: {content} to {mobile_number}")
            try:
                messanger.send_message(mobile_number, content)
                Message.update(status="pending", pending_at=datetime.datetime.utcnow()).where(Message.id == msg_id).execute()
                status = messanger.wait_and_get_msg_status()
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
