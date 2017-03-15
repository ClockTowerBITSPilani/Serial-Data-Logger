import connHandler

connHandler.test()

ard1 = connHandler.Connection()
ard1.configureManual(baudrate = 9600, port = '/dev/arduino0', timeout = 1)

ard1.run()