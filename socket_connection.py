import socketio
import time

sio = socketio.Client();
connected = False;
while not connected:
    try:
        #sio.connect("http://50.17.173.72:3000")
        sio.connect("http://localhost:3000")
        sio.emit('new_connect', 'daq_solar')
        connected = True;
    except socketio.exceptions.ConnectionError:
        print("Socket connection error.")
        time.sleep(5)


@sio.on("")
def on_message(data):
    print(data)


def send_solar(data):
    sio.emit('daq_solar', data)


def send_err(msg):
    sio.emit('err_msg', ['DAQpi:', msg])
