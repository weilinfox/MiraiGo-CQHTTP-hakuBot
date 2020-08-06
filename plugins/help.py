from hakuCore.botApi import *

def main (msgDict):
    helpMsg = '''小白现在懂得这些命令了哦:
[命令] help 获取帮助～
about
bc [args]
echo [args]
help
log [args]
ping
time [args]'''
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], helpMsg)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], helpMsg)
 
