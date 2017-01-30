class Action(object):
	def __init__(self):
		self.act = None
		self.loc = None
		self.color = None
		self.number = None

	def __str__(self):
		rep = "act:" + str(self.act) + " "
		if self.loc != None:
			rep += "loc:" + str(self.loc) + " "
		if self.color != None:
			rep += "color:" + str(self.color) + " "
		if self.number != None:
			rep += "number:" + str(self.number) + " "
		return str(rep)