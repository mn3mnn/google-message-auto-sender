from dotenv import load_dotenv
from peewee import *
from playhouse.db_url import connect
from os import getenv
from datetime import datetime

load_dotenv()

db = connect(getenv("DATABASE_URL"))


class BaseModel(Model):
    class Meta:
        database = db


class Message(BaseModel):
    id = AutoField(primary_key=True)
    content = TextField()
    mobile_number = CharField(max_length=45)
    status = CharField(max_length=45, default="unsent")
    created_at = DateTimeField(default=datetime.utcnow)
    pending_at = DateTimeField(null=True)
    sent_at = DateTimeField(null=True)
    conversation_id = CharField(max_length=45, null=True)

    def __str__(self):
        return f"Message: {self.content} to {self.mobile_number}"

    @classmethod
    def add_new_message(cls, content, mobile_number):
        cls.create(content=content, mobile_number=mobile_number)

    @classmethod
    def get_unsent_messages(cls):
        return cls.select().where(cls.status == "unsent")

    @classmethod
    def get_pending_messages(cls):
        return cls.select().where(cls.status == "pending")

    @classmethod
    def get_sent_messages(cls):
        return cls.select().where(cls.status == "sent")

    @classmethod
    def get_failed_messages(cls):
        return cls.select().where(cls.status == "failed")

    @classmethod
    def get_mobile_number(cls, msg_id):
        msg = cls.select().where(cls.id == msg_id).get()
        return msg.mobile_number

    @classmethod
    def get_content(cls, msg_id):
        msg = cls.select().where(cls.id == msg_id).get()
        return msg.content


if __name__ == "__main__":
    # db.create_tables([Message])  # uncomment this line to create tables or create the db file then comment it again

    # uncomment the below line to add new message to db, then run this file
    # Message.add_new_message("Hello", "0123456789")

    pass