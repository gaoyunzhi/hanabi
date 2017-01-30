class Card(object):
	def __init__(self, number, color):
		self.number = number
		self.color = color

	def __str__(self):
		return str(self.number) + self.color