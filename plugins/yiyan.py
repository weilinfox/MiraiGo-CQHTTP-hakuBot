# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import hakuCore.logging
import requests
import json

def main (msgDict):
    helpMsg = '传入参数，小白会搜索以下五个类别哦~\na 动画, b 漫画,\nc 文学, d 哲学\ne 诗词'
    req = list(msgDict['raw_message'].split(' ', 1))
    ans = ''
    if len(req) > 1:
        req[1] = req[1].strip()
    if len(req) > 1 and len(req[1]) > 0:
        url = 'https://v1.hitokoto.cn/'
        if req[1] == 'a':
            params = {'c':'a'}
        elif req[1] == 'b':
            params = {'c':'b'}
        elif req[1] == 'c':
            params = {'c':'d'}
        elif req[1] == 'd':
            params = {'c':'k'}
        elif req[1] == 'e':
            params = {'c':'i'}
        else:
            params = {'c':'a'}

        try:
            resp = requests.get(url=url,params=params)
            if resp.status_code == 200:
                rejson = json.loads(resp.text)
                # print(rejson)
                ans = rejson['hitokoto'] + '\n' + rejson['from']
            else:
                ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
        except Exception as e:
            
            hakuCore.logging.printLog('ERROR', 'plugin.yiyan: ' + str(e))
            ans = '啊嘞嘞好像出错了，一定是一言炸了不关小白！'
    else:
        ans = helpMsg

    return ans
 
