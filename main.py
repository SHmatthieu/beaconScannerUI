import threading
from libUI import  BtscannerUI, Beacon
import random
import time

def testFunc(ui):
    i = 1
    bs = []
    while True:
        b = Beacon("b"+str(i), random.randint(0,6), "zzzz")
        bs.append(b)
        ui.addBeacon(b)
        i+=1
        if i%3==0:
            ui.removeBeacon(bs.pop(0))
            ui.removeBeacon(bs.pop(0))
        time.sleep(2)


bt = BtscannerUI()
threading.Thread(target=testFunc, args=(bt,)).start()
bt.startUI()