import time
import mate as m
import LabJackPython

import labjack as lj
while True:
    if lj.open_labjacks():
        lj.ws.send_err('')
        startTime=time.time()
        while lj.dp_connect and lj.dm_connect: # todo: run this file on startup? Do I need a main?
            # todo: error checking. if labjacks unplugged (retry duration) if websocket can't connect ...
            try:
                lj.collect_data_panels()
                time.sleep(5.0 - ((time.time() - startTime) % 5.0)) # todo: set duration of repeat
            except LabJackPython.LabJackException:
                break


    time.sleep(15)
