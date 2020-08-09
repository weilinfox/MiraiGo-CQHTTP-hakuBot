# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from time import strftime, gmtime, time
import os
import hakuCore.botApi

lastMsgDict = {}
logFileLock = False

def startLog():
    if os.path.exists('data/log/haku.log'):
        logNo = 0
        while os.path.exists('data/log/haku.log.'+str(logNo)):
            logNo += 1
        os.rename('data/log/haku.log', 'data/log/haku.log.'+str(logNo))
    writeFile = open('data/log/haku.log', 'w')
    writeFile.write('[ ' + strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()) \
                        + ' ](启动): 开始记录日志')
    writeFile.close()

def logging(logInfo):
    global logFileLock
    while logFileLock:
        pass
    logFileLock = True
    writeFile = open('data/log/haku.log', 'a')
    writeFile.write(logInfo.replace('\r\n', '\n')+'\n')
    writeFile.close()
    logFileLock = False

def printLog(logType, logInfo):
    logStr = '\n[ ' + strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()) \
                + ' ](' + logType + '): ' + logInfo
    print(logStr)
    logging(logStr)

def directPrintLog(logInfo):
    print(logInfo)
    logging(logInfo)


def newMsgLog(msgDict):
    global lastMsgDict

    # 只留下群消息
    if not msgDict.get('raw_message'):
        return
    elif msgDict['message_type'] != 'group':
        return
    # 下面防止奇怪的复读
    if msgDict['raw_message'] == '[视频]你的QQ暂不支持查看视频短片，请升级到最新版本后查看。':
        return

    if not lastMsgDict.get(msgDict['group_id']):
        lastMsgDict.update({msgDict['group_id']:[msgDict['user_id'], msgDict['raw_message'], msgDict['time'], False]})
    else:
        if lastMsgDict[msgDict['group_id']][1] == msgDict['raw_message']:
            if not lastMsgDict[msgDict['group_id']][3] and msgDict['time'] - lastMsgDict[msgDict['group_id']][2] < 60 \
               and lastMsgDict[msgDict['group_id']][0] != msgDict['user_id']:
                try:
                    hakuCore.botApi.send_group_message(msgDict['group_id'], msgDict['raw_message'])
                except Exception as e:
                    print(e)
                    printLog('ERROR', 'logging.py: in send_group_message()')
                lastMsgDict[msgDict['group_id']][3] = True
            
            lastMsgDict[msgDict['group_id']][0] = msgDict['user_id']
            lastMsgDict[msgDict['group_id']][2] = msgDict['time']
        else:
            lastMsgDict[msgDict['group_id']] = [msgDict['user_id'], msgDict['raw_message'], msgDict['time'], False]
    
