import CBstate
if CBstate.androidos:
    import errno
    from jnius import autoclass
    bmsgcount = 0

    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')

    def breceivemsg(recv_stream):

        #while recv_stream.ready != None:
        #while recv_stream != None:
        #while True:
        try:
            line = recv_stream.readLine()
        except jnius.jnius.JavaException as e:
            print("JavaException: ", e, rfsocket.connected)
            return
        except jnius.jnius.BlockingIOError as e:
            if e.args[0] == errno.EWOULDBLOCK:
                print ('EWOULDBLOCK')
            else:
                print("BlockingIOError: ", e, rfsocket.connected)
            return
        except jnius.jnius.IOException as e:
            print("IOException: ", e, rfsocket.connected)
            return
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
        #socket.settimeout(2.0)
        return recv_stream, send_stream
else:
    import serial
    
    
