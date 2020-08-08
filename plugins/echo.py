# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.botApi import *

def main (msgDict):
    helpMsg = '''人类本质的一个实现～
由于不可告人的原因，过长的字段会被截断，包含中括号和大括号的字段可能复读失败
qaq'''
    req = list(msgDict['raw_message'].split(' ', 1))
    if msgDict['message_type'] == 'private':
        if (len(req) > 1 and req[1].strip() == 'help'):
            send_private_message(msgDict['user_id'], helpMsg)
        elif len(req) == 1 or (len(req) > 1 and len(req[1].strip()) == 0):
            send_private_message(msgDict['user_id'], '好像心里空空的…')
        else:
            send_private_message(msgDict['user_id'], req[1])
    elif msgDict['message_type'] == 'group':
        if (len(req) > 1 and req[1].strip() == 'help'):
            send_group_message(msgDict['group_id'], helpMsg)
        elif len(req) == 1 or (len(req) > 1 and len(req[1].strip()) == 0):
            send_group_message(msgDict['group_id'], '好像心里空空的…')
        else:
            send_group_message(msgDict['group_id'], req[1])
