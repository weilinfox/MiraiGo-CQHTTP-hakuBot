# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

# hakuCore
# hakubot 内核
# 接受、处理并分发 go-cqhttp 传来的 json

from importlib import import_module
import time
import hakuCore.botApi
import hakuCore.logging
import hakuCore.timeEvent

VERSION = 'v1.0.0'

dateStampList = []      # 按日日期戳 str
timeStampList = []      # 按时时间戳 str
dateTimeStampList = []  # 按日期时间戳 str

def newMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('ERROR', 'hakuCore.py: in newMsgLog()')
    else:
        plgs.insert()

def haku (msgDict):
    newMsgLog()
    
    # 分发命令
    if (msgDict.get('raw_message') and msgDict['raw_message'][0] == ':'):
        req = list(msgDict['raw_message'].split(' ', 1))
        try:
            plgs = import_module('plugins.'+req[0][1:])
        except:
            hakuCore.logging.printLog('DEBUG', 'hakuCore.py: in haku, no such plugin: ' + req[0][1:])
        else:
            plgs.main(msgDict)
            return

    # 命令以外的处理
    if msgDict.get('raw_message') and msgDict['raw_message'].strip() == '小白':
        if msgDict['message_type'] == 'private':
            hakuCore.botApi.send_private_message(msgDict['user_id'], '小白在呢~')
        elif msgDict['message_type'] == 'group':
            hakuCore.botApi.send_group_message(msgDict['group_id'], '小白在呢~')
    elif msgDict.get('raw_message'):
        for pos in range(0, len(msgDict['raw_message'])-1):
            #print(msgDict['raw_message'][pos:pos+2])
            if msgDict['raw_message'][pos:pos+2] == '小白':
                if msgDict['message_type'] == 'private':
                    hakuCore.botApi.send_private_message(msgDict['user_id'], '[CQ:face,id=175]')
                elif msgDict['message_type'] == 'group':
                    hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:face,id=175]')
                break
    elif msgDict.get('notice_type') and msgDict['notice_type'] == 'group_recall':
        #hakuCore.botApi.send_group_message(msgDict['group_id'], '{CQ:at,id=' + str(msgDict['user_id']) + '}' + '\n又有人怀孕了(小声)')
        #hakuCore.botApi.send_group_message(msgDict['group_id'], '又有人怀孕了(小声)')
        pass

    # 主动复读
    if msgDict.get('raw_message') and msgDict['message_type'] == 'group':
        try:
            hakuCore.logging.newMsgLog(msgDict)
        except:
            hakuCore.logging.printLog('ERROR', 'hakuCore.py: logging.newMsgLog(msgDict)')


def hakuTime():
    global dateStampList, timeStampList, dateTimeStampList
    tm = time.gmtime(time.time() + 8*3600)
    try:
        # 按日期通知12点检查 仅群组
        if tm.tm_hour == 0 and tm.tm_min == 0:
            tmstmp = time.strftime("%02m%02d", tm)
            if not dateStampList.count(tmstmp):
                hakuCore.timeEvent.sendGroupDate(tmstmp)
                dateStampList.append(tmstmp)
        else:
            if len(dateStampList) > 0:
                dateStampList = []

        # 每分钟检查 仅群组
        tmstmp = time.strftime("%02H%02M", tm)
        if not timeStampList.count(tmstmp):
            hakuCore.timeEvent.sendGroupTime(tmstmp)
            timeStampList = [tmstmp]
                
    except:
        hakuCore.logging.printLog('ERROR', 'hakuCore.py: in hakuTime()')
    #print(time.strftime("%02m%02d", tm))


