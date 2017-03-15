import datetime
from time import sleep
import serial
import struct


def test():
	print('This is a test')


class Connection:



	# TOKENS
	# 	\x01	RX	slave ready for handshake
	# 	\x02	TX	mastr ready for handshake
	# 	\x03	RX	Handshake done
	# 	\x11	RX	slave asking for data request
	# 	\x12	TX	master requesting immediately
	# 	\x13	TX	master requesting nothing
	# 	\x14	RX	slave asking for sending data immediately
	#	\x15	TX	master accepting immediate data



	def _init_(self):
		self.sr = serial.Serial()
		self.token = 0x00
		# END _init_()



	def configure(self):
		return 1
		# END configure()



	def configureManual(self, baudrate, port, timeout):
		self.sr = serial.Serial()
		self.sr.baudrate = baudrate
		self.sr.port = port
		self.sr.timeout = timeout
		# END configurManual()


	
	def resetPort(self):
		self.sr.setDTR(False)
		sleep(0.5)
		self.sr.reset_input_buffer()
		self.sr.setDTR(True)
		sleep(0.5)		# If less than 1, first token sent may be null
		# END resetPort()



	def tokenRead(self):
		try:
			tokenPacked = self.sr.read(1)	# tokenPacked contains bytes of len 1
			sleep(0.01)
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1

		self.token = struct.unpack('B', tokenPacked)[0]	# Unpack bytes to int tuple and take the only element
		return self.token
		
		#END tokenRead()



	def tokenWrite(self, token):

		if token not in range(0, 0x100):
			# Check for token to be 1 byte
			return -1

		tokenPacked = struct.pack('B', token)	# Pack int to bytes
		
		try:
			self.sr.reset_input_buffer()
			self.sr.write(tokenPacked)
			sleep(0.01)
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		except serial.serialutil.SerialTimeoutException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		
		return 1
		
		# END tokenWrite()



	def openPort(self):
		try:
			self.sr.close()			# Closes port if it is already open, else nothing happens. Opening an open port raises error
			self.sr.open()
			print(str(datetime.datetime.now())+'\t'+'Port opened: '+self.sr.port)
			return 1
		
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		# END openPort()



	def handshake(self):
	
		status = self.tokenWrite(0x02)

		if status == -1:
			return -1

		token = self.tokenRead()

		if token == 0x03:
			print(str(datetime.datetime.now())+'\t'+'Handshake done with '+self.sr.port)
			return 1
		elif token == 0x00:
			return -1
		else:
			return -1
		# END handshake()



	def dataidWrite(self, dataid):
		
		if dataid not in range(0, 0x10000):
			# Check for dataid to be 2 bytes
			return -1

		dataidPacked = struct.pack('<H', dataid)	#Pack int to bytes, ittle Endian

		try:
			self.sr.reset_input_buffer()
			self.sr.write(dataidPacked)
			sleep(0.01)
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		except serial.serialutil.SerialTimeoutException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		
		return 1

		#END dataidWrite



	def dataidRead(self):
		
		try:
			dataidPacked = self.sr.read(2)	# dataidPacked contains bytes of len 2
			sleep(0.01)
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		
		dataid = struct.unpack('<H', dataidPacked)[0]	# Unpack bytes to int tuple and take the only element
		return dataid
		
		# END dataidRead()



	def dataRead(self):
		
		try:
			data = self.sr.readline()
		except serial.serialutil.SerialException as e:
			print(str(datetime.datetime.now())+'\t'+str(e))
			return -1
		
		return data

		# END dataRead(ss)



	# END Connection
