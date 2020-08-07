import threading
import socket
import time
import hakuCore.config
import timer
import server
from quitAll import setQuit

def sendQuitPackage():
    try:
        ADDRESS = (hakuCore.config.HOST, hakuCore.config.RECEIVEPORT)
        msg = 'POST / HTTP/1.0\r\nX-Self-Id: 1009\r\nConnect-Length: 0\r\n\r\n'
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.connect(ADDRESS)
        server_socket.send(msg.encode('utf-8', errors='ignore'))
        rpyMsg = server_socket.recv(hakuCore.config.BUF_SIZE);
        server_socket.close()
        print('Quit package send successfully!')
    except:
        server_socket.close()
        print('Quit package send ERROR!')

def judgeServerStatus():
    global serverThread, timerThread
    if timerThread.isAlive() and serverThread.isAlive():
        return True
    elif timerThread.isAlive():
        print("\nserver.py start FAILED!\n")

        #重试5次
        retry = 0
        while retry < 5 and not serverThread.isAlive():
            print('Try to restart it within 15 seconds. (' + str(retry+1) + '/5)')
            time.sleep(15)
            #time.sleep(5)
            retry += 1
            print('Try to restart server.py ...')
            serverThread = threading.Thread(target=server.main, daemon=True)
            serverThread.start()
            time.sleep(2)
            if serverThread.isAlive():
                print('Restart successfully!\n')
                return True
            else:
                print("server.py restart FAILED!\n")

        print('Give up.')
        setQuit()
        print('Quit flag setted.')
        print('Waiting for threads...')
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    elif serverThread.isAlive():
        print("\ntimer.py start FAILED!")
        setQuit()
        print('Quit flag setted.')
        print('Waiting for threads...')
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    else:
        print("\ntimer.py and server.py start FAILED!\n")
        
    return False
    

# 配置文件检查
print("\nCheck for config errors.")



# 启动 server 和 timer
print('Starting service.')
timerThread = threading.Thread(target=timer.main, daemon=True)
serverThread = threading.Thread(target=server.main, daemon=True)
timerThread.start()
serverThread.start()

# 等待初始化完成
time.sleep(2)

if judgeServerStatus():
    print("Successful! Press Ctrl+C to quit.\n")
    #print(timerThread.isAlive(), serverThread.isAlive())
    try:
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    except KeyboardInterrupt:
        # Ctrl+C 退出
        setQuit()
        print('\nQuit flag setted.')
        # 向 server 发送一个包触发退出
        print('send quit package.')
        sendQuitPackage()

    print('Waiting for threads...')
    while timerThread.isAlive() or serverThread.isAlive():
        time.sleep(1)


print('\nWill now quit.\n')
    



