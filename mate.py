import json

import socket_connection as ws
import requests

mateIP = '192.168.0.64'
httpCall = 'http://' + mateIP + '/Dev_status.cgi'
PARAMS = {'Port': 0}

battery = ["Shunt_A_I", "Shunt_A_AH", "Shunt_A_kWh", "Shunt_B_I", "Shunt_B_AH", "Shunt_B_kWh", "SOC", "Min_SOC", "Days_since_full","CHG_parms_met", "In_AH_today", "Out_AH_today", "In_kWh_today", "Out_kWh_today", "Net_CFC_AH", "Net_CFC_kWh", "Batt_V", "Batt_temp"]
chargeController = ["Out_I", "In_I", "Batt_V", "In_V", "Out_kWh", "Out_AH"]
inverter = ["Inv_I", "Chg_I", "Buy_I", "Sell_I", "VAC_in", "VAC_out", "Batt_V"]

def addmate3data(jsonFile):
    try:
        r = requests.get(url=httpCall, params=PARAMS)
        data = r.json
        # Fetch all of these from the Mate 3s
        # Change the port number to match the corresponding object.
        tmpBatt = data['ports'][0] # Battery
        tmpPCC = data['ports'][1] # Poly Charge Controller
        tmpMCC = data['ports'][2] # Mono Charge Controller
        tmpInv = data['ports'][3] # Inverter
        for x in range(0, len(battery) - 1):
            jsonFile.Battery[battery[x]] = tmpBatt[battery[x]]
        for x in range(0, len(chargeController) - 1):
            jsonFile.ChargeControllerM[chargeController[x]] = tmpMCC[chargeController[x]]
            jsonFile.ChargeControllerP[chargeController[x]] = tmpPCC[chargeController[x]]
        for x in range(0, len(inverter) - 1):
            jsonFile.Inverter[inverter[x]] = tmpInv[inverter[x]]

    except requests.exceptions.RequestException as e:
        print e
        jsonFile.Battery = {"Shunt_A_I": 0, "Shunt_A_AH": 0, "Shunt_A_kWh": 0.0, "Shunt_B_I": 0.0, "Shunt_B_AH": 0, "Shunt_B_kWh": 0.000, "SOC": 0, "Min_SOC": 0, "Days_since_full": 0.0,"CHG_parms_met": False, "In_AH_today": 0, "Out_AH_today": 0, "In_kWh_today": 0.0, "Out_kWh_today": 0.0, "Net_CFC_AH": 0, "Net_CFC_kWh": 0.0, "Batt_V": 0.0, "Batt_temp": 0.0}
        for x in range(len(chargeController) - 1):
            jsonFile.ChargeControllerP[chargeController[x]] = 0.0
            jsonFile.ChargeControllerM[chargeController[x]] = 0.0
        for x in range(len(inverter) - 1):
            jsonFile.Inverter[inverter[x]] = 0

    json_data = json.dumps(jsonFile)
    ws.send_solar(json_data)
