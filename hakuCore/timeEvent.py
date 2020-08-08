import os
import hakuCore.botApi
import hakuCore.logging

groups = []

def load():
    global groups
    hakuCore.logging.directPrintLog('loading data...')
    groups = os.listdir('data/groupDay')
    hakuCore.logging.directPrintLog('load ' + str(len(groups)) + ' group-days.')



def searchGroup(group, date):
    # int group, int date(mmdd)
    global groups
    groupFile = str(group)
    daten = int(date)
    if not groups.count(groupFile):
        return ''
    else:
        ans = '';
        firstLine = True
        readFile = open('data/groupDay/'+groupFile, 'r')
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
                pass
        readFile.close()
        return ans

def searchGroupDate(date):
    # int date(mmdd)
    global groups
    ans = {}
    for grps in groups:
        if not grps[0].isdigit():
            continue
        grpstr = searchGroup(grps, date)
        if len(grpstr) > 0:
            ans.update({int(grps):grpstr})
    return ans

def sendGroup(grps, date):
    groupNo = int(grps)
    daten = int(date)
    msg = searchGroup(groupNo, daten)
    if len(msg) > 0:
        hakuCore.botApi.send_group_message(groupNo, msg)

def sendGroupDate(date):
    daten = int(date)
    msgDict = searchGroupDate(daten)
    if len(msgDict) > 0:
        for key in msgDict.keys():
            hakuCore.botApi.send_group_message(key, msgDict[key])
        
if __name__ == '__main__':
    load()
