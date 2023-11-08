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
    content = TextField(null=False)
    mobile_number = CharField(max_length=20, null=False)
    status = CharField(max_length=45, default="unsent")
    added_at = DateTimeField(default=datetime.utcnow)
    pending_at = DateTimeField(null=True)
    sent_at = DateTimeField(null=True)
    # account_id = TextField(null=True)
    # user_id/user_key = TextField(null=True) not null

    def __str__(self):
        return f"Message: {self.content} to {self.mobile_number}"

    @classmethod
    def add_new_message(cls, content, mobile_number):
        msg = cls.create(content=content, mobile_number=mobile_number)
        return msg

    @classmethod
    def get_msg(cls, msg_id):
        return cls.select().where(cls.id == msg_id).get()

    @classmethod
    def get_messages_by_status(cls, status):
        return cls.select().where(cls.status == status)

    @classmethod
    def get_status(cls, msg_id):
        msg = cls.select().where(cls.id == msg_id).get()
        return msg.status

    @classmethod
    def set_msg_status(cls, msg_id, status):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.status = status
        msg.save()

    @classmethod
    def set_msg_pending_at(cls, msg_id, pending_at):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.pending_at = pending_at
        msg.save()

    @classmethod
    def set_msg_sent_at(cls, msg_id, sent_at):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.sent_at = sent_at
        msg.save()


if __name__ == "__main__":
    db.create_tables([Message])  # create tables if not exists

    # uncomment the below line to add new message to db, then run this file
    # Message.add_new_message("Hello", "0123456789")
