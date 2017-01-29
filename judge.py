
from const import NUM_CARDS_IN_HAND
from const import TOKEN_INIT

class Judge(object):
	def __init__(self):
		pass

	def takeDeck(self, deck):
		self._deck = deck

	def takePlayer(self, player1, player2):
		self._player1 = player1
		self._player2 = player2
		self._hand = {self._player1: [], self._player2: []}

	def start(self):
		for _ in xrange(NUM_CARDS_IN_HAND):
			self._sendCard(self._player1, self._getCard())
			self._sendCard(self._player2, self._getCard())
	
	def _sendCard(self, player, card):
		self._hand[player].append(card)
		

	def _getCard(self):
		if self._deck:
			return self._deck.pop(0)	


