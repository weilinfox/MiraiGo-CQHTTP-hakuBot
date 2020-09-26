# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import os
import importlib
import hakuCore.botApi
import hakuCore.logging
import hakuCore.config

groupDays = []
groupTimes = []
writeLock = False
readLock = False

def load():
    global groupDays, groupTimes
    hakuCore.logging.directPrintLog('loading data...')
    # 写时不可读
    while writeLock:
        pass
    readLock = True
    groupDays = os.listdir('data/groupDay')
    groupTimes = os.listdir('data/groupTime')
    readLock = False
    hakuCore.logging.directPrintLog('load ' + str(len(groupDays)) + ' group-days.')
    hakuCore.logging.directPrintLog('load ' + str(len(groupTimes)) + ' group-times.')

def mwrite():
    # 读时不可写
    while readLock:
        pass
    writeLock = True
    writeLock = False

def searchGroup(dirname, group, date):
    # int group, int date(mmdd)/time(hhmm)
    # 从对应 dirname 文件夹中读取 group 对应配置
    # 匹配 date 或 time
    # 写时不可读
    while writeLock:
        pass
    readLock = True
    if not os.path.exists('data/' + dirname):
        hakuCore.logging.printLog('错误', 'in timeEvent.py: 没有 data/' \
                                  + dirname + '这个目录')
        readLock = False
        return ''
    
    groupFile = str(group)
    daten = int(date)
    if not os.path.exists('data/' + dirname + '/' + groupFile):
        hakuCore.logging.printLog('错误', 'in timeEvent.py: 没有 data/' \
                                  + dirname + '/' + groupFile + '这个文件')
        readLock = False
        return ''
    else:
        ans = '';
        firstLine = True
        readFile = open('data/' + dirname + '/' + groupFile, 'r')
        while True:
            line = readFile.readline()
            if len(line) == 0:
                break
            lineList = list(line.replace('\n', '').split())
            if len(lineList) < 2:
                continue
    
            try:
                lineDate = int(lineList[0])
                if lineDate == daten:
                    if firstLine:
                        firstLine = False
                    else:
                        ans += '\n'
                    for pos in range(1, len(lineList)):
                        if pos != 1:
                            ans += ' '
                        ans += lineList[pos]
            except:
                hakuCore.logging.printLog('ERROR', 'in timeEvent.py: searchGroup(' \
                                          + dirname + ', ' + groupFile + ', ' + str(date) + ')')
        readFile.close()
        readLock = False
        return ans

def searchGroupDate(date):
    # int date(mmdd)
    global groupDays
    ans = {}
    com = {}
    for grps in groupDays:
        grpstr = searchGroup('groupDay', grps, date)
        if len(grpstr) > 0:
            grplist = list(grpstr.split('\n'))
            message = ''
            command = []
            for s in grplist:
                if s[0] == hakuCore.config.PREFIX:
                    command.append(s)
                else:
                    if len(message) == 0: message = s
                    else: message += '\n' + s
            if len(message) > 0: ans.update({int(grps):message})
            if len(command) > 0: com.update({int(grps):command})
    return [ans,com]

def searchGroupTime(tm):
    # int tm(hhmm)
    global groupTimes
    ans = {}
    com = {}
    for grps in groupTimes:
        grpstr = searchGroup('groupTime', grps, tm)
        if len(grpstr) > 0:
            grplist = list(grpstr.split('\n'))
            message = ''
            command = []
            for s in grplist:
                if s[0] == hakuCore.config.PREFIX:
                    command.append(s)
                else:
                    if len(message) == 0: message = s
                    else: message += '\n' + s
            if len(message) > 0: ans.update({int(grps):message})
            if len(command) > 0: com.update({int(grps):command})
    return [ans,com]

#def sendGroup(dirname, grps, date):
#    groupNo = int(grps)
#    daten = int(date)
#    msg = searchGroup(dirname, groupNo, daten)
#    if len(msg) > 0:
#        hakuCore.botApi.send_group_message(groupNo, msg)

def sendGroupDate(date):
    daten = int(date)
    msgDict = searchGroupDate(daten)
    if len(msgDict[0]) > 0:
        for key in msgDict[0].keys():
            hakuCore.botApi.send_group_message(key, msgDict[0][key])
    if len(msgDict[1]) > 0:
        for key in msgDict[1].keys():
            for com in msgDict[1][key]:
                msgHead = list(com.split())[0]
                try:
                    plgs = importlib.import_module('plugins.' + msgHead[1:])
                except:
                    hakuCore.logging.printLog('ERROR', 'plugins.' + msgHead[1:] + '.py: no such plugin.')
                else:
                    try:
                        nMsgDict = {'group_id':key, 'message':com, 'message_type':'group', 'post_type':'message', 'raw_message':com, 'post_type':'message'}
                        plgs.main(nMsgDict)
                    except:
                        hakuCore.logging.printLog('ERROR', 'plugins.' + msgHead[1:] + '.py: ERROR occurred in this plugin.')

def sendGroupTime(tm):
    tmn = int(tm)
    msgDict = searchGroupTime(tmn)
    if len(msgDict[0]) > 0:
        for key in msgDict[0].keys():
            hakuCore.botApi.send_group_message(key, msgDict[0][key])
    if len(msgDict[1]) > 0:
        for key in msgDict[1].keys():
            for com in msgDict[1][key]:
                msgHead = list(com.split())[0]
                try:
                    plgs = importlib.import_module('plugins.' + msgHead[1:])
                except:
                    hakuCore.logging.printLog('ERROR', 'plugins.' + msgHead[1:] + '.py: no such plugin.')
                else:
                    try:
                        nMsgDict = {'group_id':key, 'message':com, 'message_type':'group', 'post_type':'message', 'raw_message':com, 'post_type':'message'}
                        plgs.main(nMsgDict)
                    except:
                        hakuCore.logging.printLog('ERROR', 'plugins.' + msgHead[1:] + '.py: ERROR occurred in this plugin.')
        
if __name__ == '__main__':
    load()
