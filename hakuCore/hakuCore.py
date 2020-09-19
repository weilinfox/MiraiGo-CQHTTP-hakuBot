# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

# hakuCore
# hakubot 内核
# 接受、处理并分发 go-cqhttp 传来的 json

from importlib import import_module
from hakuCore.config import INTERVAL, PREFIX
import time
import threading
import hakuCore.botApi
import hakuCore.logging
import hakuCore.timeEvent

VERSION = 'v1.0.14'

dateStampList = []      # 按日日期戳 [str]
timeStampList = []      # 按时时间戳 [str]
dateTimeStampList = []  # 按日期时间戳 [str]
threadDict = {}         # 线程字典 {thread:time}

def checkMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('INFO', 'hakuCore.py: log plugin NOT found')
    else:
        plgs.check()
    return

def getMsgRate():
    try:
        plgs = import_module('plugins.log')
    except:
        return 'Log plugin NOT found.'
    else:
        return str(plgs.msgRate()) + '/min, ' + 'heart rate: ' + str(plgs.heartRate())  + '/min'

def newMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('INFO', 'hakuCore.py: log plugin NOT found')
    else:
        plgs.insert()

def newHeartBeat():
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('INFO', 'hakuCore.py: log plugin NOT found')
    else:
        plgs.heartBeats()

def threadInfo(thr, timeout):
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('INFO', 'hakuCore.py: log plugin NOT found')
    else:
        plgs.threadStatus(thr, timeout)

def hakuMain (msgDict):
    atMe = '[CQ:at,qq=' + str(msgDict['self_id']) + ']' # haku被at的cq码

    # 被at
    if msgDict.get('raw_message') and msgDict['message_type'] == 'group' and msgDict['raw_message'].count(atMe):
        hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:at,qq=' + str(msgDict['user_id']) + ']\n' + '找小白有啥事咩，可以发送"' + PREFIX + 'help"获取帮助哦~')
        return

    newMsgLog()

    # 分发命令
    if (msgDict.get('raw_message') and msgDict['raw_message'][0] == PREFIX):
        req = list(msgDict['raw_message'].split(' ', 1))
        try:
            plgs = import_module('plugins.'+req[0][1:])
        except:
            hakuCore.logging.printLog('DEBUG', 'hakuCore.py: in haku, no such plugin: ' + req[0][1:])
            return
        else:
            try:
                plgs.main(msgDict)
            except:
                hakuCore.logging.printLog('ERROR', 'plugins.' + req[0][1:] + '.py: ERROR occurred in this plugin.')
            return

    # 命令以外的处理
    if msgDict.get('raw_message') and msgDict['raw_message'].strip() == '小白':
        if msgDict['message_type'] == 'private':
            hakuCore.botApi.send_private_message(msgDict['user_id'], '有小白在，不会有事的')
        elif msgDict['message_type'] == 'group':
            hakuCore.botApi.send_group_message(msgDict['group_id'], '有小白在，不会有事的')
    elif msgDict.get('raw_message'):
        if msgDict['raw_message'].count('小白'):
            if msgDict['message_type'] == 'private':
                hakuCore.botApi.send_private_message(msgDict['user_id'], '[CQ:face,id=175]')
            elif msgDict['message_type'] == 'group':
                hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:face,id=175]')
        elif msgDict['raw_message'].count('犬夜叉'):
            if msgDict['message_type'] == 'private':
                hakuCore.botApi.send_private_message(msgDict['user_id'], '犬夜叉是坠吼的!')
            elif msgDict['message_type'] == 'group':
                hakuCore.botApi.send_group_message(msgDict['group_id'], '犬夜叉是坠吼的!')
    elif msgDict.get('notice_type') and msgDict['notice_type'] == 'group_recall':
        #hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:at,qq=' + str(msgDict['user_id']) + ']' + '\n又有人怀孕了(小声)')
        #hakuCore.botApi.send_group_message(msgDict['group_id'], '又有人怀孕了(小声)')
        pass

    # 主动复读
    if msgDict.get('raw_message') and msgDict['message_type'] == 'group':
        try:
            hakuCore.logging.newMsgLog(msgDict)
        except:
            hakuCore.logging.printLog('ERROR', 'hakuCore.py: logging.newMsgLog(msgDict)')

    # 欢迎新人
    # 指定群回复群号为int 键值为空时不回复指定的群
    groupIncreaseReply = {
        722237880:'欢迎欢迎！',
        'else':'欢迎欢迎，进了群就是一家人了~'
        }
    if msgDict.get('notice_type') and msgDict['notice_type'] == 'group_increase':
        if groupIncreaseReply.get(msgDict['group_id']) != None and len(groupIncreaseReply[msgDict['group_id']]) > 0:
            hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:at,qq=' + str(msgDict['user_id']) + ']\n' + groupIncreaseReply[msgDict['group_id']])
        elif groupIncreaseReply.get(msgDict['group_id']) != None and len(groupIncreaseReply[msgDict['group_id']]) == 0:
            pass
        elif groupIncreaseReply.get('else') != None and len(groupIncreaseReply['else']) > 0:
            hakuCore.botApi.send_group_message(msgDict['group_id'], '[CQ:at,qq=' + str(msgDict['user_id']) + ']\n' + groupIncreaseReply['else'])

def haku(MsgDict):
    global threadDict

    hakuThread = threading.Thread(target=hakuMain, args=[MsgDict], daemon=True)
    threadDict.update({hakuThread:time.time()})
    hakuThread.start()


pmsgr = '-1/min'
nmsgr = '0/min'
checkDelay = INTERVAL * 15

def hakuHeart(msgDict):
    global dateStampList, timeStampList, dateTimeStampList, threadDict
    global pmsgr, nmsgr, checkDelay

    newHeartBeat() # 心率记录
    checkMsgLog() # 刷新消息频率缓存
    timeOutThr = 0 # 超时线程
    for thr in list(threadDict.keys()):
        if not thr.isAlive():
            threadDict.pop(thr)
        elif time.time() - threadDict[thr] >= 10:
            timeOutThr += 1
    if timeOutThr > 0:
        hakuCore.logging.printLog('WARNING', str(timeOutThr) + ' threads are detected timeout')
    threadInfo(len(threadDict), timeOutThr) # 线程池数据记录
    if checkDelay == INTERVAL * 15:
        hakuCore.timeEvent.load() # 重载时间事件
        checkDelay = 0
    checkDelay += 1
    # 打印小白流量
    nmsgr = getMsgRate()
    if pmsgr != nmsgr:
        hakuCore.logging.printLog('速率', nmsgr)
    pmsgr = nmsgr


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


