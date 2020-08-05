# hakuCore
# hakubot 内核
# 接受并处理 go-cqhttp 传来的 json

from botApi import *

def haku (msgList):
    if msgList['message_type'] == 'private' and msgList['raw_message'] == ':ping':
        send_private_message(msgList['user_id'], 'pong!')
    elif msgList['message_type'] == 'group' and msgList['raw_message'] == ':ping':
        send_group_message(msgList['group_id'], 'pong!')
        
