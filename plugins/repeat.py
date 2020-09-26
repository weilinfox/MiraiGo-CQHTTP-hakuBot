# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.botApi import *

def main (msgDict):
    req = list(msgDict['raw_message'].split(' ', 1))
    if len(req) > 1:
        req[1] = req[1].strip()
        if len(req[1]) == 0: return
    else:
        return

    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], req[1])
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], req[1])
 
