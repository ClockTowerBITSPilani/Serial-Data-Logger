import queue
import sched

class Schedule:



	def _init_(self):
		self.qu = queue.Queue()
		self.cfg = None
		self.configure()
		# END _init_()



	def empty(self):
		return self.qu.empty()
		# END empty()



	def configure(self):
		pass
		# END configure()



	def get(self):
		return self.qu.get()
		# END get()



	def update(self):
		pass
		# END update()




	# END Schedule