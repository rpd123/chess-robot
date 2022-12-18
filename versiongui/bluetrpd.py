import CBstate
if CBstate.androidos:
    import errno
    from jnius import autoclass
    msgcount = 0
    defaultCharBufferSize = 8192
    socket = None
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    InputStreamReader = autoclass('java.io.InputStreamReader')
    BufferedReader = autoclass('java.io.BufferedReader')
    
    def breceivemsg(sp):
        
        reader = InputStreamReader(socket.getInputStream())
        sp = BufferedReader(reader, defaultCharBufferSize).decode('utf-8').rstrip()
        
    '''       
    def bsendmsg(send_stream):
            send_stream = socket.getOutputStream()
    '''    
        
    UUID = autoclass('java.util.UUID')

    def get_socket_stream(name):
        global socket
        
        paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        socket = None
        for device in paired_devices:
            if device.getName() == name:
                socket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                #reader = InputStreamReader(socket.getInputStream(), getEncode)
                reader = InputStreamReader(socket.getInputStream())
                recv_stream = BufferedReader(reader, defaultCharBufferSize)
                send_stream = socket.getOutputStream()
                break
        socket.connect()
        return recv_stream, send_stream
else:
    import serial
    
    
