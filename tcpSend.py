import socket
import json
from time import strftime, gmtime
from config import HOST, SENDPORT, BUF_SIZE, TOKEN, TESTQQID

ADDRESS = (HOST, SENDPORT)

def sendMessage (msg):
    try:
        timeStr = strftime("Date: %a, %m %b %Y %H:%M:%S GMT", gmtime())
        print('\n[', timeStr, '](发送): ', msg, end='')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(ADDRESS)
        server_socket.send(msg.encode('utf-8', errors='ignore'))
        rpyMsg = server_socket.recv(BUF_SIZE);

        strHead, strBody = rpyMsg.split(b'\r\n\r\n', 1)
        strHead = strHead.decode('utf-8')
        dataLength = 0  # 数据长度
        for it in list(strHead.split("\r\n")):
            itmName, itmData = it.split(" ", 1)
            if itmName == "Content-Length:":
                dataLength = int(itmData)
                break
        while len(strBody) < dataLength:
            rpyMsg = server_socket.recv(BUF_SIZE)
            if (len(rpyMsg) == 0):
                break;
            strBody += rpyMsg

        strBody = strBody.decode('utf-8')
        server_socket.close()

        print('成功!')

        return json.loads(strBody)
    #except KeyboardInterrupt:
    #    pass
    except:
        server_socket.close()
        print('错误!')
        return {'retcode': -1, 'status': 'tcpSendError'}


def encodePost (apiStr, dataDict):
    # 我不知道是不是Miraigo不支持post，反正一直返回 {"data":null,"retcode":100,"status":"failed"}
    dataStr = json.dumps(dataDict)
    return 'POST /' + apiStr + '?access_token=' + TOKEN \
               + ' HTTP/1.0\r\nUser-Agent: haku-bot\r\n' \
               + 'Connect-Type: application/json; charset=utf-8\r\n' \
               + 'Connect-Length: ' + str(len(dataStr.encode('utf-8', errors='ignore'))) \
               + '\r\n\r\n' + dataStr

def encodeGet (apiStr, dataDict):
    msg = 'GET /' + apiStr + '?access_token=' + TOKEN
    for key in dataDict.keys():
        msg += '&' + key + '=' + str(dataDict[key])
    return msg + ' HTTP/1.0\r\n\r\n'

def uploadMessage (apiStr, dataDict):
    # 使用Get方法，模拟HTTP/1.0
    return sendMessage(encodeGet(apiStr, dataDict))


if __name__ == '__main__':
    #api = "send_group_msg"
    api = "send_private_msg"
    dataDict = {'user_id':TESTQQID, 'message': 'ping'}
    #print('\n****post request****\n\n', encodePost(api, dataDict))
    #print('\n****sendMessage return****\n\n', sendMessage(encodePost(api, dataDict)))

    print('\n****get request****\n\n', encodeGet(api, dataDict))
    print('\n****sendMessage return (-1: error)****\n\n', uploadMessage(api, dataDict), '\n')
