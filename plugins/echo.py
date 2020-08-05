from hakuCore.botApi import *

def main (msgList):
    helpMsg = '''人类本质的一个实现～
由于不可告人的原因，过长的字段会被截断，包含中括号和大括号的字段可能复读失败
qaq'''
    req = list(msgList['raw_message'].split(' ', 1))
    if msgList['message_type'] == 'private':
        if (req[1].strip() == 'help'):
            send_private_message(msgList['user_id'], helpMsg)
        else:
            send_private_message(msgList['user_id'], req[1])
    elif msgList['message_type'] == 'group':
        if (req[1].strip() == 'help'):
            send_group_message(msgList['group_id'], helpMsg)
        else:
            send_group_message(msgList['group_id'], req[1])
