from hakuCore.botApi import *

def main (msgDict):
    aboutMsg = '''小白~
是狸开发的qq机器人~'''
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], aboutMsg)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], aboutMsg) 
