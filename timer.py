from time import time, sleep
from hakuCore.config import INTERVAL
from quitAll import quitNow

def main():
    while not quitNow():
        try:
            sleep(INTERVAL)
            print('\n10s passed')
        except KeyboardInterrupt:
            break
        except:
            pass

    print("\nBye~ from timer")
