import socketio

sio = socketio.Client();

sio.connect("http://localhost:3000")


@sio.on("")
def on_message(data):
    print(data);


def send_solar(data):
    sio.emit('daq_solar', data)
