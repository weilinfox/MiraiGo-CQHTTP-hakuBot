from hakuCore.botApi import *

def main (msgList):
    helpMsg = '''小白现在懂得这些命令了哦:
[命令] help 获取帮助～
bc [args]
echo [args]
help
ping'''
    if msgList['message_type'] == 'private':
        send_private_message(msgList['user_id'], helpMsg)
    elif msgList['message_type'] == 'group':
        send_group_message(msgList['group_id'], helpMsg)
 
