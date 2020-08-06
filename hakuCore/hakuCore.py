# hakuCore
# hakubot 内核
# 接受、处理并分发 go-cqhttp 传来的 json

from importlib import import_module
from hakuCore.botApi import *

def newMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        pass
    else:
        plgs.insert()
    return

def haku (msgDict):
    newMsgLog()
    
    # 分发命令
    if (msgDict['raw_message'][0] == ':'):
        req = list(msgDict['raw_message'].split(' ', 1))
        try:
            plgs = import_module('plugins.'+req[0][1:])
        except:
            pass
        else:
            plgs.main(msgDict)
            return

    # 命令以外的处理
    if msgDict['raw_message'].strip() == '小白':
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], '小白在呢~')
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], '小白在呢~')
    else:
        for pos in range(0, len(msgDict['raw_message'])-1):
            #print(msgDict['raw_message'][pos:pos+2])
            if msgDict['raw_message'][pos:pos+2] == '小白':
                if msgDict['message_type'] == 'private':
                    send_private_message(msgDict['user_id'], '[CQ:face,id=175]')
                elif msgDict['message_type'] == 'group':
                    send_group_message(msgDict['group_id'], '[CQ:face,id=175]')
                break
