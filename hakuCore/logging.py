from time import strftime, gmtime

def printLog(logType, logInfo):
    print('\n[', strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()),
           '](' + logType + '): ', logInfo)
