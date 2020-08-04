import socket
from time import strftime, gmtime
from config import HOST, RECEIVEPORT, BUF_SIZE

ADDRESS = (HOST, RECEIVEPORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)
server_socket.listen(1)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

REPLY = "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 0\r\nServer: weilinfox-virHttp\r\n"

print("\n\nCtrl+C to quit.\n\n\n")

while True:
    try:    
        client_socket, address = server_socket.accept()
        #print(address)

        # 获取头
        postData = client_socket.recv(BUF_SIZE)
        postHead, postBody = postData.decode('utf-8').split("\r\n\r\n", 1);

        dataLength = 0  # 数据长度
        myId = 0        # bot的QQ ID
        for it in list(postHead.split("\r\n")):
            itmName, itmData = it.split(" ", 1)
            if itmName == "Content-Length:":
                dataLength = int(itmData)
            elif itmName == "X-Self-Id:":
                myId = int(itmData)

        # 超长数据
        while len(postBody.encode('utf-8')) < dataLength:
            postData = client_socket.recv(BUF_SIZE)
            if (len(postData) == 0):
                break;
            postBody += postData.decode('utf-8')

        # 响应
        rplStr = REPLY + strftime("Date: %a, %m %b %Y %H:%M:%S GMT", gmtime()) + "\r\n\r\n"
        client_socket.send(rplStr.encode('utf-8', errors='ignore'))

        print(postBody)

    except KeyboardInterrupt:
        break
    except:
        pass

print("\n\n\n\nBye~\n\n")
server_socket.close()

