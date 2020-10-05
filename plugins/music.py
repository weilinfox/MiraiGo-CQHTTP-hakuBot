# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import socket
import json

HOST = 'inuyasha.love'
PORT = 8001
URL = 'http://inuyasha.love:8001/'

ADDRESS = (HOST, PORT)

def encodeMsg (msg):
    msg = msg.replace('%', '%25')
    msg = msg.replace('&', '%26')
    msg = msg.replace('=', '%3D')
    msg = msg.replace('+', '%2B')
    msg = msg.replace('\n', ' ')
    msg = msg.replace('/', '%2F')
    msg = msg.replace('#', '%23')
    msg = msg.replace('?', '%3F')
    msg = msg.replace('!', '%21')
    msg = msg.replace('*', '%2A')
    msg = msg.replace('"', '%22')
    msg = msg.replace("'", '%27')
    msg = msg.replace('(', '%28')
    msg = msg.replace(')', '%29')
    msg = msg.replace(';', '%3B')
    msg = msg.replace(':', '%3A')
    msg = msg.replace('@', '%40')
    msg = msg.replace('$', '%24')
    msg = msg.replace(',', '%2C')
    msg = msg.replace(' ', "%20")
    msg = str(msg.encode('utf-8', errors='ignore')).replace('\\x', '%')[2:][:-1]

    return 'GET ' + URL + 'search?keywords=' + msg + ' HTTP/1.0\r\n\r\n'
    

def main (msgDict):
    helpMsg = '小白会试着从网易云搜索~'
    req = list(msgDict['raw_message'].split(' ', 1))
    ans = ''
    if len(req) > 1:
        req[1] = req[1].strip()
    if len(req) > 1 and len(req[1]) > 0:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(ADDRESS)
        server_socket.send(encodeMsg(req[1]).encode('utf-8', errors='ignore'))
        tmpbuf = server_socket.recv(2048)
        rebuf = b''
        while len(tmpbuf):
            rebuf += tmpbuf
            tmpbuf = server_socket.recv(2048)
        restr = list(rebuf.decode('utf-8').split('\r\n'))
        rejson = json.loads(restr[len(restr)-1])
        if rejson['code'] == 200:
            if rejson['result'].get('songs'):
                mscid = rejson['result']['songs'][0]['id']
                mscname = rejson['result']['songs'][0]['name']
                ans = '[CQ:share,url=https://music.163.com/song/' + str(mscid) + '/,title=' + str(mscname) + ']'
            else:
                ans = '网易云里没有诶~'
        else:
            ans = '好像返回了奇怪的东西: ' + str(rejson['code'])
    else:
        ans = helpMsg

    return ans
