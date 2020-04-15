import json

import socket_connection as ws

def addmate3data(jsonFile):
    # Fetch all of these from the Mate 3s
    jsonFile.Battery = ''
    jsonFile.ChargeControllerP = ''
    jsonFile.ChargeControllerM = ''
    jsonFile.Inverter = ''
    json_data = json.dumps(jsonFile)
    ws.send_solar(json_data)

