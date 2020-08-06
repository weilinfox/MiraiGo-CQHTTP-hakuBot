from hakuCore.botApi import *

def main (msgDict):
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], 'pong!')
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], 'pong!')
