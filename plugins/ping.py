from hakuCore.botApi import *

def main (msgList):
    if msgList['message_type'] == 'private':
        send_private_message(msgList['user_id'], 'pong!')
    elif msgList['message_type'] == 'group':
        send_group_message(msgList['group_id'], 'pong!')
