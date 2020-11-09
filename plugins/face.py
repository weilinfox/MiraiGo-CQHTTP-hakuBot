# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import hakuCore.logging
import requests
import json

allowGroup = [1091802120]

def main (msgDict):
    url = 'http://cloud1.catop.top:81/qqbot-face/getimg-1.php'
    age = 0
    req = list(msgDict['raw_message'].split(' ', 1))
    try:
        age = int(req[1])
    except:
        age = 200
    if msgDict['message_type'] != 'group':
        age = 200
    elif not allowGroup.count(msgDict['group_id']):
        age = 200

    ans = ''

    try:
        resp = requests.get(url=url,params={'age':age})
        if resp.status_code == 200:
            # print(resp.text)
            ans = '[CQ:image,file=' + resp.text + ']'
        else:
            ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
    except Exception as e:
        hakuCore.logging.printLog('ERROR', 'plugin.face: ' + str(e))
        ans = '啊嘞嘞好像出错了，啊啊啊不关小白！'

    return ans
 
