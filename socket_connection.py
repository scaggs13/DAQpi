import socketio

sio = socketio.Client();
try:
    sio.connect("http://localhost:3000")
except socketio.exceptions.ConnectionError:
    print("Socket connection error.")

@sio.on("connect")
def on_connect():
    sio.emit('new_connect', 'daq_solar')

@sio.on("")
def on_message(data):
    print(data);


def send_solar(data):
    sio.emit('daq_solar', data)


def send_err(msg):
    sio.emit('err_msg', msg)
