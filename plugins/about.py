from hakuCore.botApi import *
from hakuCore.hakuCore import VERSION

def main (msgDict):
    aboutMsg = '小白哥哥是狸开发的qq机器人~\n'
    aboutMsg += '小白是小白哥哥 ' + VERSION + ' 的分身!'
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], aboutMsg)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], aboutMsg) 
