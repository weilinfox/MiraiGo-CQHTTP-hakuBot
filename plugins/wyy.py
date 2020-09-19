# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.botApi import *
import hakuCore.logging
import requests
import json

def main (msgDict):
    helpMsg = '今天小白不高兴[CQ:face,id=107]'
    req = list(msgDict['raw_message'].split(' ', 1))
    ans = ''
    if len(req) > 1:
        ans = helpMsg
    else:
        try:
            resp = requests.get(url='https://v1.hitokoto.cn/',params={'c':'j'})
            if resp.status_code == 200:
                rejson = json.loads(resp.text)
                # print(rejson)
                ans = rejson['hitokoto']
            else:
                ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
        except Exception as e:
            hakuCore.logging.printLog('ERROR', 'plugin.wyy: ' + str(e))
            ans = '啊嘞嘞好像出错了，一定是一言炸了不关小白！'

    if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], ans)
    elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], ans)
 
