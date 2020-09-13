# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import threading
import os
import socket
import time
import hakuCore.config
import server
from quitAll import setQuit
from hakuCore.logging import directPrintLog, startLog

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
    global serverThread
    if serverThread.isAlive():
        return True
    else:
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
        
    return False

def checkDir():
    # 判断data文件夹是否存在
    if os.path.exists('data'):
        if os.path.isdir('data'):
            print('Data dir found.')
        else:
            os.rename('data', 'data.old')
            os.mkdir('data')
    else:
        print('Create data dir.')
        os.mkdir('data')

    # 判断data/log文件夹是否存在
    if os.path.exists('data/log'):
        if os.path.isdir('data/log'):
            print('Log dir found.')
        else:
            os.rename('data/log', 'data/log.old')
            os.mkdir('data/log')
    else:
        print('Create log dir.')
        os.mkdir('data/log')

    # 判断data/groupDay文件夹是否存在
    if os.path.exists('data/groupDay'):
        if os.path.isdir('data/groupDay'):
            print('GroupDay dir found.')
        else:
            os.rename('data/groupDay', 'data/groupDay.old')
            os.mkdir('data/groupDay')
    else:
        print('Create groupDay dir.')
        os.mkdir('data/groupDay')

    # 判断data/groupTime文件夹是否存在
    if os.path.exists('data/groupTime'):
        if os.path.isdir('data/groupTime'):
            print('GroupTime dir found.')
        else:
            os.rename('data/groupTime', 'data/groupTime.old')
            os.mkdir('data/groupTime')
    else:
        print('Create groupTime dir.')
        os.mkdir('data/groupTime')


# 检测 data 文件夹
checkDir()

# 初始化日志
startLog()

# 配置文件检查
directPrintLog("\nCheck for config errors...")

# 启动 server 和 timer
directPrintLog('Starting service.')
serverThread = threading.Thread(target=server.main, daemon=True)
serverThread.start()

# 等待初始化完成
time.sleep(2)

if judgeServerStatus():
    directPrintLog("Successful! Press Ctrl+C to quit.\n")
    #print(timerThread.isAlive(), serverThread.isAlive())
    try:
        while serverThread.isAlive():
            time.sleep(1)
    except KeyboardInterrupt:
        # Ctrl+C 退出
        setQuit()
        directPrintLog('\nQuit flag setted.')
        # 向 server 发送一个包触发退出
        directPrintLog('send quit package.')
        sendQuitPackage()

    directPrintLog('Waiting for threads...')
    while serverThread.isAlive():
        time.sleep(1)


directPrintLog('\nWill now quit.\n')
    



