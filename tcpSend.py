import socket
from config import HOST, SENDPORT, BUF_SIZE, TOKEN, TESTQQID

ADDRESS = (HOST, SENDPORT)

def sendMessage (msg):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(ADDRESS)
        server_socket.send(msg.encode('utf-8'))
        rpyMsg = server_socket.recv(BUF_SIZE);
        print('\n****Mirai return:****\n\n', rpyMsg.decode('utf-8'))
        server_socket.close()
        return 0
    except:
        return -1


def encodePost (api, data):
    return 'POST /' + api + '?access_token=' + TOKEN \
               + ' HTTP/1.0\r\nUser-Agent: haku-bot\r\n' \
               + 'Connect-Type: application/json; charset=utf-8\r\n' \
               + 'Connect-Length: ' + str(len(data.encode('utf-8', errors='ignore'))) \
               + '\r\n\r\n' + data
    

if __name__ == '__main__':
    data = '{"user_id": ' + str(TESTQQID) + ', "message": "hello"}'
    api = "send_private_msg"
    print('\n****post request****\n\n', encodePost(api, data), end='\n\n')
    print('\n****sendMessage return: ****\n\n', sendMessage(encodePost(api, data)))
