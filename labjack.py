import u3
import json
import socket_connection as ws
import mate as mate
from LabJackPython import LabJackException

global dm_connect, dp_connect, dm, dp
dm = None;
dp = None;

# Define JSON
data_poly = {"PolyP1v": 0, "PolyP2v": 0, "PolyP3v": 0, "A3": 0, "PolyP1i": 0, "PolyP2i": 0, "PolyP3i": 0, "F7": 0}
tmp_poly = []

data_mono = {"MonoP1v": 0, "MonoP2v": 0, "MonoP3v": 0, "A3": 0, "MonoP1i": 0, "MonoP2i": 0, "MonoP3i": 0, "F7": 0}
tmp_mono = []

dm_connect = False
dp_connect = False

# Define conversion factors
ORDER_POLY = ["PolyP1v", "PolyP2v", "PolyP3v", "A3", "PolyP1i", "PolyP2i", "PolyP3i", "F7"]
POLY_HV_CONVERSION_MULT = 8.425154
POLY_HV_CONVERSION_ADD = -10.313406
ORDER_MONO = ["MonoP1v", "MonoP2v", "MonoP3v", "A3", "MonoP1i", "MonoP2i", "MonoP3i", "F7"]
MONO_HV_CONVERSION_MULT = 8.555073
MONO_HV_CONVERSION_ADD = -10.472785
CONVERSION = [1, 1, 1, 1, 1, 1, 1, 1]  # todo: change these values
# todo: error checking


def open_labjacks():
    global dm, dp, dp_connect, dm_connect
    try:
        if not dm_connect:
            # Open Mono Panels' LabJack
            dm = u3.U3(autoOpen=False)
            dm.open(handleOnly=True, serial=320090158)
            dm.configIO(FIOAnalog=255)  # Set every input to analog
            dm_connect = True;
    except LabJackException:
        print("Connection Error to LabJack: Cannot find Mono LabJack")
        if dm:
            dm.close()
        if dp:
            dp.close()
        ws.send_err('Cannot find Mono LabJack');
        return False
    try:
        if not dp_connect:
            # Open Poly Panels' LabJack
            dp = u3.U3(autoOpen=False)
            dp.open(handleOnly=True, serial=320087751)
            dp.configIO(FIOAnalog=255)  # Set every input to analog
            # dp.writeRegister(5000, 3) # testing
            dp_connect = True;
    except LabJackException:
        print("Connection Error to LabJack: Cannot find Poly LabJack")
        if dm:
            dm.close()
        if dp:
            dp.close()
        ws.send_err('Cannot find Poly LabJack');
        return False
    return True


def collect_data_panels():
    if dm_connect and dp_connect:
        try:
            # Collect data first time
            for x in range(0, 8):
                tmp_poly.append(dp.getAIN(x, 32))
                tmp_mono.append(dm.getAIN(x, 32))
            # Get average of 100 data points
            for x in range(0, 100):
                for y in range(0, 8):
                    tmp_poly[y] = (tmp_poly[y] + dp.getAIN(y, 32)) / 2
                    tmp_mono[y] = (tmp_mono[y] + dm.getAIN(y, 32)) / 2
            # Convert Values
            for x in range(0, 8):
                if x < 4:
                    tmp_poly[x] = tmp_poly[x]*POLY_HV_CONVERSION_MULT+POLY_HV_CONVERSION_ADD
                    tmp_mono[x] = tmp_mono[x]*MONO_HV_CONVERSION_MULT+MONO_HV_CONVERSION_ADD
                tmp_poly[x] = tmp_poly[x] * CONVERSION[x]
                tmp_mono[x] = tmp_mono[x] * CONVERSION[x]
            # Save to JSON Object
            for x in data_poly:
                data_poly[x] = tmp_poly[ORDER_POLY.index(x)]
            for x in data_mono:
                data_mono[x] = tmp_mono[ORDER_MONO.index(x)]

            tmp_json = {"Mono": data_mono, "Poly": data_poly}
            mate.addmate3data(tmp_json)
            # Dump JSON
            # json_data = json.dumps(tmp_json)
            # ws.send_solar(json_data)
            print(json_data) # todo: get rid of this line.
            # Clear temp lists
            del tmp_poly[:]
            del tmp_mono[:]
        except:
            print("error")
            try:
                dp.getAIN(0)
            except:
                global dp_connect
                dp_connect = False
                dp.close()
            try:
                dm.getAIN(0)
            except:
                global dm_connect
                dm_connect = False
                dm.close()
    else:
        if not dm_connect:
            print("Mono labjack not connected")
        if not dp_connect:
            print("Poly labjack not connected")


def __del__(self):
    dm.close() # Close Mono Panels' LabJack
    dp.close() # Close Poly Panels' LabJack
