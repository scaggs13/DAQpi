import time
import labjack as lj

startTime=time.time()
while True: # todo: run this file on startup? Do I need a main?
    # todo: error checking. if labjacks unplugged (retry duration) if websocket can't connect ...
    lj.collect_data_panels()
    time.sleep(5.0 - ((time.time() - startTime) % 5.0)) # todo: set duration of repeat
