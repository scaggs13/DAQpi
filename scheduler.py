import time
import mate as m
import LabJackPython

import labjack as lj        # <---- If solar uncomment this and comment out the line below
import windLabjack as wlj   # <---- If wind uncomment this and comment out the line above

while True:
    # If solar uncomment the if statement below and comment out the bottom if statement.
    if lj.open_labjacks():
        lj.ws.send_err('')
        lj.ws.connect_solar()
        startTime=time.time()
        while lj.dp_connect and lj.dm_connect: # todo: run this file on startup? Do I need a main?
            # todo: error checking. if labjacks unplugged (retry duration) if websocket can't connect ...
            try:
                lj.collect_data_panels()
                time.sleep(5.0 - ((time.time() - startTime) % 5.0)) # todo: set duration of repeat
            except LabJackPython.LabJackException:
                break

    # If wind uncomment the if statement below and comment out the if statement above.
    if wlj.open_labjacks():
        wlj.ws.send_err('')
        wlj.ws.connect_wind()
        startTime=time.time()
        while wlj.d2_connect and wlj.d1_connect: # todo: run this file on startup? Do I need a main?
            # todo: error checking. if labjacks unplugged (retry duration) if websocket can't connect ...
            try:
                wlj.collect_data()
                time.sleep(5.0 - ((time.time() - startTime) % 5.0)) # todo: set duration of repeat
            except LabJackPython.LabJackException:
                break


    time.sleep(15)
