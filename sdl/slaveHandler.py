import connHandler
import dataHandler
import schedHandler

class Device:

	stateDict = {
		'error':	-1,
		'start':	0,
		'closed':	1,
		'opened':	2,
		'rdy4hs':	3,
		'synced':	4,
		'canrq':	5,
		'has2rxm':	6,
		'rdy2rxm':	7,
		'hasnorq':	8,
		'hasrq':	9,
		'rqing':	10,
		'rdy2rx':	11,
		'hasdata':	12
	}



	def _init_(self):
		self.state = stateDict['start']
		self.conn = connHandler.Connection()
		self.schd = schedHandler.Schedule()
		self.token = None
		self.data = None
		self.dataid = None
		self.attemptFails = {
			'opening':	0,
			'initiate':	0,
			'handshake':	0
		}



	def configure(self):
		return 1
		# END configure()



	def configureManual(self):
		return 1
		# END configureManual()



	def tokenReset(self):
		self.token = 0x00
		# END tokenRest()



	def run(self):

		while True:

			if self.state == self.stateDict['start']:
				
				if self.configure() == 1:
					# Configuration successfull
					self.state = stateDict['closed']
				
				else:
					# Configuration failed
					pass

			
			
			elif self.state == self.stateDict['closed']:
				
				status = self.conn.openPort()

				if status == 1:
					# Port opening successfull
					self.state = stateDict['opened']
				
				elif status == -1:
					# Port opening failed
					pass

				else:

					pass
			
			
			
			elif self.state == self.stateDict['opened']:
				
				self.token = self.conn.tokenRead()

				if self.token == 0x01:
				
					self.state = self.stateDict['ready4hs']
					self.tokenReset()	# Avoid reusing this token again
				
				elif self.token == -1:
				
					self.conn.resetPort()
					self.state = self.stateDict['opened']
				
				else:
				
					pass
			
			
			
			elif self.state == stateDict['ready4hs']:
				
				status = self.conn.handshake()

				if status == 1:
					# Handshake successfull
					self.state = self.stateDict['synced']
				
				elif status == -1:
					# Handshake unsuccessfull
					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:

					pass
			
			
			
			elif self.state == stateDict['synced']:
			
				self.token = self.conn.tokenRead()

				if self.token == 0x11:

					self.state = self.stateDict['canrq']
					self.tokenReset()	# Avoid reusing this token again

				elif self.token == 0x21:

					self.state = self.stateDict['has2rx']
					self.tokenReset()	# Avoid reusing this token again
				
				elif self.token == -1:

					self.conn.resetPort()
					self.state = self.stateDict['opened']
				
				else:

					pass
			
			
			
			elif self.state == stateDict['canrq']:

				self.schd.update()
				
				if self.dataid != None or self.schd.empty() == False:
					self.state = self.stateDict['hasrq']

				elif self.dataid == None and self.schd.empty() == True:
					self.state = self.stateDict['hasnorq']


			
			elif self.state == stateDict['has2rx']:
				
				status = self.conn.tokenWrite(0x22)

				if status == 1:
					# Token write succesfull	
					self.state = self.stateDict['rdy2rxm']
				
				elif status == -1:
					# SerialException
					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:
					
					pass
			
			
			
			elif self.state == stateDict['rdy2rxm']:
				
				dataid = self.conn.dataidRead()

				if dataid == -1:

					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:
					self.data = self.conn.dataRead()

					if self.data == -1:
						
						self.conn.resetPort()
						self.state = self.stateDict['opened']

					else:
						self.state = self.stateDict['hasdata']

	
			
			elif self.state == stateDict['hasnorq']:
				
				status = self.conn.tokenWrite(0x13)

				if status == 1:
					# Token write succesfull	
					self.state = self.stateDict['synced']
				
				elif status == -1:
					# SerialException
					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:
					
					pass
			
			
			
			elif self.state == stateDict['hasrq']:
				
				status = self.conn.tokenWrite(0x12)

				if status == 1:
					# Token write succesfull	
					self.state = self.stateDict['rqing']
				
				elif status == -1:
					# SerialException
					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:
					
					pass
			
			

			elif self.state == stateDict['rqing']:

				if self.dataid == None:
					self.dataid = self.schd.get()
				
				status = self.conn.dataidWrite(self.dataid)

				if status == 1:
					# dataid write succesfull	
					self.state = self.stateDict['rdy2rx']
				
				elif status == -1:
					# SerialException
					self.conn.resetPort()
					self.state = self.stateDict['opened']

				else:
					
					pass
						
			
			
			elif self.state == stateDict['rdy2rx']:
				
				dataid = self.conn.dataidRead()

				if dataid == -1:

					self.conn.resetPort()
					self.state = self.stateDict['opened']

				elif dataid == dataidBuffer:

					self.data = self.conn.dataRead()

					if self.data == -1:
						
						self.conn.resetPort()
						self.state = self.stateDict['opened']

					else:
						self.state = self.stateDict['hasdata']

				else:
					pass

			

			elif self.state == stateDict['hasdata']:
				
				status = dataHandler.record(self.dataid, self.data)

				if status == 1:
				
					self.data = None
					self.dataid = None
					self.state = self.stateDict['synced']
				
				elif status == -1:

					self.conn.resetPort()
					self.state = self.stateDict['opened']

		# END run()

	

	#END Device