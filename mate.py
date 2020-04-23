import json
import labjack as lj
import requests

mateIP = '173.218.91.129:3000'
httpCall = 'http://' + mateIP + '/Dev_status.cgi'
PARAMS = {'Port': 0}

battery = ["Shunt_A_I", "Shunt_A_AH", "Shunt_A_kWh", "SOC", "Min_SOC", "Days_since_full","CHG_parms_met", "In_AH_today", "Out_AH_today", "In_kWh_today", "Out_kWh_today", "Net_CFC_AH", "Net_CFC_kWh", "Batt_V", "Batt_temp"]
chargeController = ["Out_I", "In_I", "Batt_V", "In_V", "Out_kWh", "Out_AH"]
inverter = ["Inv_I_L2","Chg_I_L2","Buy_I_L2","Sell_I_L2","VAC1_in_L2","VAC2_in_L2","VAC_out_L2","Batt_V"]


def addmate3data(jsonFile):
    jsonFile['Battery'] = {}
    jsonFile['ChargeControllerM'] = {}
    jsonFile['ChargeControllerP'] = {}
    jsonFile['Inverter'] = {}
    try:
        r = requests.get(url=httpCall, params=PARAMS)
        data = r.json()
        # Fetch all of these from the Mate 3s
        # Change the port number to match the corresponding object.
        for x in range(0, len(data)):
            print x
        for x in range(0, len(data['devstatus']['ports'])):
            if data['devstatus']['ports'][x]['Port'] == 4:
                tmpBatt = data['devstatus']['ports'][x]  # Battery
            else:
                tmpBatt = None
            if data['devstatus']['ports'][x]['Port'] == 3:
                tmpPCC = data['devstatus']['ports'][x]  # Poly Charge Controller
            else:
                tmpPCC = None
            if data['devstatus']['ports'][x]['Port'] == 2:
                tmpMCC = data['devstatus']['ports'][x]  # Mono Charge Controller
            else:
                tmpMCC = None
            if data['devstatus']['ports'][x]['Port'] == 1:
                tmpInv = data['devstatus']['ports'][x]  # Inverter
            else:
                tmpInv = None
        if tmpBatt:
            print(len(battery))
            for x in range(0, len(battery)):
                if battery[x] == "Batt_temp":
                    if tmpBatt[battery[x]] != "###":
                        tmpBatt[battery[x]] = float(tmpBatt[battery[x]].replace(' C',''))
                    else:
                        tmpBatt[battery[x]] = 0
                jsonFile['Battery'][battery[x]] = tmpBatt[battery[x]]
            print(jsonFile)
        for x in range(0, len(chargeController)):
            if tmpMCC:
                jsonFile['ChargeControllerM'][chargeController[x]] = tmpMCC[chargeController[x]]
            if tmpPCC:
                jsonFile['ChargeControllerP'][chargeController[x]] = tmpPCC[chargeController[x]]
        if tmpInv:
            for x in range(0, len(inverter)):
                jsonFile['Inverter'][inverter[x]] = tmpInv[inverter[x]]
        print(jsonFile)
    except requests.exceptions.RequestException as e:
        print e
        jsonFile['Battery'] = {"Shunt_A_I": 0, "Shunt_A_AH": 0, "Shunt_A_kWh": 0.0, "SOC": 0, "Min_SOC": 0, "Days_since_full": 0.0,"CHG_parms_met": False, "In_AH_today": 0, "Out_AH_today": 0, "In_kWh_today": 0.0, "Out_kWh_today": 0.0, "Net_CFC_AH": 0, "Net_CFC_kWh": 0.0, "Batt_V": 0.0, "Batt_temp": 0.0}
        for x in range(len(chargeController)):
            jsonFile['ChargeControllerP'][chargeController[x]] = 0.0
            jsonFile['ChargeControllerM'][chargeController[x]] = 0.0
        for x in range(len(inverter)):
            jsonFile['Inverter'][inverter[x]] = 0

    print(jsonFile)
    json_data = json.dumps(jsonFile)
    lj.ws.send_solar(json_data)
