import u3
import json
import socket_connection as ws
from LabJackPython import LabJackException


d1 = None
d2 = None

# Define JSON
data_3phase = {"P31_V": 0, "P32_V": 0, "P33_V": 0, "A3": 0, "P31_I": 0, "P32_I": 0, "P33_I": 0, "F7": 0}
tmp_3phase = []

data_load = {"Load_V": 0, "Batt_V": 0, "A2": 0, "A3": 0, "Load_I": 0, "Batt_I": 0, "F6": 0, "F7": 0}
tmp_load = []

d1_connect = False
d2_connect = False

# Define conversion factors
ORDER_3P = ["P31_V", "P32_V", "P33_V", "A3", "P31_I", "P32_I", "P33_I", "F7"]
# Insert Conversion Factors here
# For High Voltage Conversion
P3_HV_CONVERSION_ADD1 = 0            # Add before multiply
P3_HV_CONVERSION_MULT = 8.425154     # multiply factor
P3_HV_CONVERSION_ADD2 = -10.313406   # Add after multiply
ORDER_LOAD = ["Load_V", "Batt_V", "A2", "A3", "Load_I", "Batt_I", "F6", "F7"]
# Insert Conversion Factors here
# For High Voltage Conversion
LOAD_HV_CONVERSION_ADD1 = 0             # Add before multiply
LOAD_HV_CONVERSION_MULT = 8.555073      # multiply factor
LOAD_HV_CONVERSION_ADD2 = -10.472785    # Add after multiply

# Sensor conversions
# Three Phase Order follows ORDER_3P variable above
CONVERSION_P3_MULT = [1, 1, 1, 1, 1, 1, 1, 1]  # Multiply factor for sensors. todo: change these values
CONVERSION_P3_ADD1 = [0, 0, 0, 0, 0, 0, 0, 0] # Add before multiply
CONVERSION_P3_ADD2 = [0, 0, 0, 0, 0, 0, 0, 0] # Add after multiply

# Load Order follows ORDER_LOAD variable above
CONVERSION_LOAD_MULT = [1, 1, 1, 1, 1, 1, 1, 1]  # Multiply factor for sensors. todo: change these values
CONVERSION_LOAD_ADD1 = [0, 0, 0, 0, 0, 0, 0, 0] # Add before multiply
CONVERSION_LOAD_ADD2 = [0, 0, 0, 0, 0, 0, 0, 0] # Add after multiply
# todo: error checking


def open_labjacks():
    global d1, d2, d2_connect, d1_connect
    try:
        if not d1_connect:
            # Open Load LabJack
            d1 = u3.U3(autoOpen=False)
            d1.open(handleOnly=True, serial=320090158)  # Change this to match serial of Load labjack.(Connected to Load and Battery)
            d1.configIO(FIOAnalog=255)  # Set every input to analog
            d1_connect = True;
    except LabJackException:
        print("Connection Error to LabJack: Cannot find Load LabJack")
        if d1:
            d1.close()
        if d2:
            d2.close()
        ws.send_err('Cannot find Load LabJack');
        return False
    try:
        if not d2_connect:
            # Open Poly Panels' LabJack
            d2 = u3.U3(autoOpen=False)
            d2.open(handleOnly=True, serial=320087751)  # Change this to match serial of 3 Phase Labjack
            d2.configIO(FIOAnalog=255)  # Set every input to analog
            # dp.writeRegister(5000, 3) # testing
            d2_connect = True;
    except LabJackException:
        print("Connection Error to LabJack: Cannot find 3 phase LabJack")
        if d1:
            d1.close()
        if d2:
            d2.close()
        ws.send_err('Cannot find 3 phase LabJack');
        return False
    return True


def collect_data():
    global d1_connect, d2_connect
    if d1_connect and d2_connect:
        try:
            # Collect data first time
            for x in range(0, 8):
                tmp_3phase.append(d2.getAIN(x, 32))
                tmp_load.append(d1.getAIN(x, 32))
            # Get average of 100 data points
            for x in range(0, 100):
                for y in range(0, 8):
                    tmp_3phase[y] = (tmp_3phase[y] + d2.getAIN(y, 32)) / 2
                    tmp_load[y] = (tmp_load[y] + d1.getAIN(y, 32)) / 2
            # Convert Values
            for x in range(0, 8):
                if x < 4:
                    tmp_3phase[x] = (tmp_3phase[x] + P3_HV_CONVERSION_ADD1) * P3_HV_CONVERSION_MULT + P3_HV_CONVERSION_ADD2
                    tmp_load[x] = (tmp_load[x] + LOAD_HV_CONVERSION_ADD1) * LOAD_HV_CONVERSION_MULT + LOAD_HV_CONVERSION_ADD2
                tmp_3phase[x] = (tmp_3phase[x] + CONVERSION_P3_ADD1[x]) * CONVERSION_P3_MULT[x] + CONVERSION_P3_ADD2[x]
                tmp_load[x] = (tmp_load[x] + CONVERSION_LOAD_ADD1[x]) * CONVERSION_P3_MULT[x] + CONVERSION_LOAD_ADD2[x]
            # Save to JSON Object
            for x in data_3phase:
                data_3phase[x] = tmp_3phase[ORDER_3P.index(x)]
            for x in data_load:
                data_load[x] = tmp_load[ORDER_LOAD.index(x)]

            tmp_json = {"P31_V": tmp_3phase[0], "P32_V": tmp_3phase[1], "P33_V": tmp_3phase[2], "A3": tmp_3phase[3], "P31_I": tmp_3phase[4], "P32_I": tmp_3phase[5], "P33_I": tmp_3phase[6], "F7": tmp_3phase[07],
                        "Load_V": tmp_load[0], "Batt_V": tmp_load[1], "A2": tmp_load[2], "A3": tmp_load[3], "Load_I": tmp_load[4], "Batt_I": tmp_load[5], "F6": tmp_load[6], "F7": tmp_load[7]}
            # Dump JSON
            json_data = json.dumps(tmp_json)
            ws.send_wind(json_data)
            # print(json_data) # todo: get rid of this line.
            # Clear temp lists
            del tmp_3phase[:]
            del tmp_load[:]
        except:
            print("error")
            try:
                d2.getAIN(0)
            except:
                global d2_connect
                d2_connect = False
                d2.close()
            try:
                d1.getAIN(0)
            except:
                global d1_connect
                d1_connect = False
                d1.close()
    else:
        if not d1_connect:
            print("Load labjack not connected")
        if not d2_connect:
            print("3 Phase labjack not connected")


def __del__(self):
    d1.close() # Close Mono Panels' LabJack
    d2.close() # Close Poly Panels' LabJack
