'''
Bluetooth/Pyjnius example
=========================
This was used to send some bytes to an arduino via bluetooth.
The app must have BLUETOOTH and BLUETOOTH_ADMIN permissions (well, i didn't
tested without BLUETOOTH_ADMIN, maybe it works.)
Connect your device to your phone, via the bluetooth menu. After the
pairing is done, you'll be able to use it in the app.
'''
from jnius import autoclass
import time
msgcount = 0

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')

def receivemsg(recv_stream):
    global msgcount
    msgcount += 1

    while recv_stream.ready != None:
        try:
            line = recv_stream.readLine()
        except jnius.jnius.JavaException as e:
            print("JavaException: ", e, rfsocket.connected)
            
        except ValueError as e:
            print("Misc error: ", e)

        try:
            print(msgcount, line)
        except ValueError:
            pass
    
    
UUID = autoclass('java.util.UUID')

def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    for device in paired_devices:
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    return recv_stream, send_stream

if __name__ == '__main__':
    recv_stream, send_stream = get_socket_stream('HC-05')
    #send_stream.write('hello\n')
    #send_stream.flush()
    #print(recv_stream.readline())
    #send_stream.write('hello again\n')
    #send_stream.flush()
    #print(recv_stream.readline())
    
    # init steppers
    time.sleep(0.2)
    send_stream.write(("G28" + "\r").encode())   # steppers off, initialize
    send_stream.flush()
    time.sleep(0.2)
    receivemsg(recv_stream)
    time.sleep(0.2)
    
    # steppers on
    input("Press Enter to switch on steppers and start game")
    something = TextInput('Happy Christmas', 'Press Enter to switch on steppers and start game')
    something = TextInput(text='Press Enter to switch on steppers and start game')
    send_stream.write(("M17" + "\r").encode())   # Switch on steppers
    send_stream.flush()
    time.sleep(0.2)
    receivemsg(recv_stream)
    time.sleep(0.2)
    receivemsg(recv_stream)
    
    gstring = "G1" + " X0" + " Y200" + " Z60" + "\r"
    send_stream.write(gstring.encode())
    send_stream.flush()
    time.sleep(0.2)
    receivemsg(recv_stream)