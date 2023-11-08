import os

from flask import Flask, request, jsonify
from db import Message
from urls import *

API_KEYS = ['123456']

msg_json_template = {
    'ID': None,
    'attachments': None,
    'deliveredDate': None,
    'deviceID': None,
    'errorCode': None,
    'expiryDate': None,
    'groupID': None,
    'message': None,
    'number': None,
    'prioritize': None,
    'resultCode': None,
    'retries': None,
    'schedule': None,
    'sentDate': None,
    'simSlot': None,
    'status': None,
    'type': None,
    'userID': None
}

response_json_template = {
    'data': {
        'messages': []
    },
    'error': None,
    'success': True
}


app = Flask(__name__)


@app.route(SEND_MSG_ROUTE, methods=['POST', 'GET'])
def send_message():
    response_json = response_json_template.copy()
    msg_json = msg_json_template.copy()
    try:
        data = request.json
        message = data.get('message', None)
        mobile_number = data.get('number', None)
        key = data.get('key', None)
        devices = data.get('devices', None)
        type = data.get('type', None)
        prioritize = data.get('prioritize', None)

        if not all([message, mobile_number, key]):
            response_json['error'] = 'Invalid request'
            response_json['success'] = False
            return jsonify(response_json), 400

        if key not in API_KEYS:
            response_json['error'] = 'Unauthorized'
            response_json['success'] = False
            return jsonify(response_json), 401

        try: # Insert message into the database
            msg = Message.add_new_message(message, mobile_number)

            msg_json['ID'] = msg.id
            msg_json['message'] = msg.content
            msg_json['number'] = msg.mobile_number
            msg_json['status'] = msg.status
            msg_json['type'] = 'sms'
            response_json['data']['messages'].append(msg_json)
            return jsonify(response_json), 200

        except Exception as e:
            response_json['error'] = "db error, couldn't send the message"
            response_json['success'] = False
            return jsonify(response_json), 500

    except Exception as e:
        response_json['error'] = "Server error, couldn't send the message"
        response_json['success'] = False
        return jsonify(response_json), 500


#
# @app.route(GET_MSG_ROUTE, methods=['GET'])
# def get_messages():
#     response_json = response_json_template.copy()
#     msg_json = msg_json_template.copy()
#
#     try:
#         msg_id = request.args.get('id', None)
#         status = request.args.get('status', None)
#
#         if msg_id:
#             try:
#                 msg = Message.get_msg(msg_id)
#
#                 msg_json['ID'] = msg.id
#                 msg_json['message'] = msg.content
#                 msg_json['number'] = msg.mobile_number
#                 msg_json['status'] = msg.status
#                 msg_json['type'] = 'sms'
#                 response_json['data']['messages'].append(msg_json)
#                 return jsonify(response_json), 200
#
#             except Exception as e:
#                 response_json['error'] = "db error, couldn't get the message"
#                 response_json['success'] = False
#                 return jsonify(response_json), 500
#
#         elif status:
#             try:
#                 if status == 'unsent':
#                     messages = Message.get_unsent_messages()
#                 elif status == 'pending':
#                     messages = Message.get_pending_messages()
#                 elif status == 'sent':
#                     messages = Message.get_sent_messages()
#                 elif status == 'failed':
#                     messages = Message.get_failed_messages()
#                 else:
#                     response_json['error'] = 'Invalid msg status'
#                     response_json['success'] = False
#                     return jsonify(response_json), 400
#
#                 for msg in messages:
#                     msg_json['ID'] = msg.id
#                     msg_json['message'] = msg.content
#                     msg_json['number'] = msg.mobile_number
#                     msg_json['status'] = msg.status
#                     msg_json['type'] = 'sms'
#                     response_json['data']['messages'].append(msg_json)
#
#                 return jsonify(response_json), 200
#
#             except Exception as e:
#                 response_json['error'] = "db error, couldn't get the messages"
#                 response_json['success'] = False
#                 return jsonify(response_json), 500
#
#         else:
#             response_json['error'] = 'Invalid request'
#             response_json['success'] = False
#             return jsonify(response_json), 400
#
#     except Exception as e:
#         response_json['error'] = "Server error, couldn't get the messages"
#         response_json['success'] = False
#         return jsonify(response_json), 500


if __name__ == '__main__':
    app.run(debug=True)  # port=5000

