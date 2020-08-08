import os
import hakuCore.botApi

groups = []

def load():
    global groups
    print('loading data...')
    
    # 判断data文件夹是否存在
    if os.path.exists('data'):
        if os.path.isdir('data'):
            print('data dir found')
        else:
            os.rename('data', 'data.old')
            os.mkdir('data')
    else:
        os.mkdir('data')
        
    # 判断data/group文件夹是否存在
    if os.path.exists('data/group'):
        if os.path.isdir('data/group'):
            print('group dir found')
            groups = os.listdir('data/group')
            #print(os.listdir('data/group'))
            #print(os.listdir('data/'))
            print('load ' + str(len(groups)) + ' groups')
        else:
            os.rename('data/group', 'data/group.old')
            os.mkdir('data/group')
    else:
        os.mkdir('data/group')

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
        readFile = open('data/group/'+groupFile, 'r')
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
