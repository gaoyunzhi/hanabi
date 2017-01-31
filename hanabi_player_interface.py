class HanabiPlayerInterface(object):

	def act(self):
		raise NotImplementedError

	def postAct(self, action, card, player_index):
		pass



