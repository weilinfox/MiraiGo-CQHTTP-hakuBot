import threading
import socket
import time
import hakuCore.config
import timer
import server
from quitAll import setQuit
from hakuCore.logging import directPrintLog

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
        directPrintLog('Quit package send successfully!')
    except:
        server_socket.close()
        directPrintLog('Quit package send ERROR!')

def judgeServerStatus():
    global serverThread, timerThread
    if timerThread.isAlive() and serverThread.isAlive():
        return True
    elif timerThread.isAlive():
        directPrintLog("\nserver.py start FAILED!\n")

        #重试5次
        retry = 0
        while retry < 5 and not serverThread.isAlive():
            directPrintLog('Try to restart it within 15 seconds. (' + str(retry+1) + '/5)')
            time.sleep(15)
            #time.sleep(5)
            retry += 1
            directPrintLog('Try to restart server.py ...')
            serverThread = threading.Thread(target=server.main, daemon=True)
            serverThread.start()
            time.sleep(2)
            if serverThread.isAlive():
                directPrintLog('Restart successfully!\n')
                return True
            else:
                directPrintLog("server.py restart FAILED!\n")

        directPrintLog('Give up.')
        setQuit()
        directPrintLog('Quit flag setted.')
        directPrintLog('Waiting for threads...')
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    elif serverThread.isAlive():
        directPrintLog("\ntimer.py start FAILED!")
        setQuit()
        directPrintLog('Quit flag setted.')
        directPrintLog('Waiting for threads...')
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    else:
        directPrintLog("\ntimer.py and server.py start FAILED!\n")
        
    return False
    

# 配置文件检查
directPrintLog("\nCheck for config errors.")



# 启动 server 和 timer
directPrintLog('Starting service.')
timerThread = threading.Thread(target=timer.main, daemon=True)
serverThread = threading.Thread(target=server.main, daemon=True)
timerThread.start()
serverThread.start()

# 等待初始化完成
time.sleep(2)

if judgeServerStatus():
    directPrintLog("Successful! Press Ctrl+C to quit.\n")
    #print(timerThread.isAlive(), serverThread.isAlive())
    try:
        while timerThread.isAlive() or serverThread.isAlive():
            time.sleep(1)
    except KeyboardInterrupt:
        # Ctrl+C 退出
        setQuit()
        directPrintLog('\nQuit flag setted.')
        # 向 server 发送一个包触发退出
        directPrintLog('send quit package.')
        sendQuitPackage()

    directPrintLog('Waiting for threads...')
    while timerThread.isAlive() or serverThread.isAlive():
        time.sleep(1)


directPrintLog('\nWill now quit.\n')
    



