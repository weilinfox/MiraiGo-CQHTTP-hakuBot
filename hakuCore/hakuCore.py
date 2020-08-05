# hakuCore
# hakubot 内核
# 接受、处理并分发 go-cqhttp 传来的 json

from importlib import import_module
from hakuCore.botApi import *

def haku (msgList):
    # 分发命令
    if (msgList['raw_message'][0] == ':'):
        req = list(msgList['raw_message'].split(' ', 1))
        try:
            plgs = import_module('plugins.'+req[0][1:])
        except:
            pass
        else:
            plgs.main(msgList)
            return

    # 命令以外的处理
    if msgList['raw_message'].strip() == '小白':
        if msgList['message_type'] == 'private':
            send_private_message(msgList['user_id'], '小白在呢~')
        elif msgList['message_type'] == 'group':
            send_group_message(msgList['group_id'], '小白在呢~')
    else:
        for pos in range(0, len(msgList['raw_message'])-1):
            #print(msgList['raw_message'][pos:pos+2])
            if msgList['raw_message'][pos:pos+2] == '小白':
                if msgList['message_type'] == 'private':
                    send_private_message(msgList['user_id'], '[CQ:face,id=175]')
                elif msgList['message_type'] == 'group':
                    send_group_message(msgList['group_id'], '[CQ:face,id=175]')
                break
