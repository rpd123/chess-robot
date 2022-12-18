#import CBstate
if CBstate.androidos:
    #import errno
    from jnius import autoclass
    bmsgcount = 0
    rfsocket = None
    device = None
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    InputStreamReader = autoclass('java.io.InputStreamReader')
    BufferedReader = autoclass('java.io.BufferedReader')

    def get_socket_stream(name):
        global rfsocket, device
        defaultCharBufferSize = 8192
        try:
            blueAdapt = BluetoothAdapter.getDefaultAdapter()
            if rfsocket is not None:
                if rfsocket.connected:
                    reader = InputStreamReader(rfsocket.getInputStream(), getEncode)
                    sp = BufferedReader(reader)
                    send_stream = rfsocket.getOutputStream()
                else:
                    rfsocket = device.createRfcommSocketToServiceRecord(UUID.fromString(getUuid))
                    if get_port_connect():
                        reader = InputStreamReader(rfsocket.getInputStream(), getEncode)
                        sp = BufferedReader(reader, defaultCharBufferSize)
                        send_stream = rfsocket.getOutputStream()
            else:
                if blueAdapt is not None:
                    if blueAdapt.isEnabled():
                        paired_devices = blueAdapt.getBondedDevices().toArray()
                        rfsocket = None
                        for device in paired_devices:
                            if device.getName() == name:
                                if device.bluetoothEnabled:
                                    rfsocket = device.createRfcommSocketToServiceRecord(
                                        UUID.fromString(getUuid))
                                    if rfsocket is not None:
                                        if get_port_connect(): #connect and set the port before creating java objects
                                            reader = InputStreamReader(rfsocket.getInputStream(), getEncode)
                                            sp = BufferedReader(reader, defaultCharBufferSize)
                                            send_stream = rfsocket.getOutputStream()
                                            break
                    else:
                        print('Bluetooth not enabled')
            if sp is not None and send_stream is not None:
                return sp, send_stream
            else:
                return False, False
        except UnboundLocalError as e:
            return False, False
        except TypeError as e:
            return False, False
    def get_port_connect():
        global rfsocket
        try:
            if rfsocket.port <= 0:
                rfsocket = device.createRfcommSocket(1) #set the port explicitly
                if not rfsocket.connected:
                    rfsocket.connect()
            else:
                if not rfsocket.connected:
                    rfsocket.connect()
            if rfsocket.connected:
                print('Connected')
            return True
        except jnius.jnius.JavaException as e:
            print('Cannot connect to socket')
            return False


            
