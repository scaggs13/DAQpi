import time
import labjack as lj

startTime=time.time()
while True:
    lj.collectDataPanels()
    time.sleep(5.0 - ((time.time() - startTime) % 5.0))
