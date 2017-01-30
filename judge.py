import msvcrt as m
from const import NUM_CARDS_IN_HAND
from const import TOKEN_INIT
from const import ACTION_PLAY
from const import ACTION_DISCARD
from const import ACTION_HINT
from const import COLOR
from const import BOOM_LIMIT
from const import ROUND_AFTER_DECK_EMPTY

class Judge(object):
	def __init__(self):
		pass

	def takeDeck(self, deck):
		self._deck = deck
		self.desk = {}
		self.discardedDeck = []
		self.boom = 0
		self.token = TOKEN_INIT
		for c in COLOR:
			self.desk[c] = 0

	def takePlayer(self, players):
		self._players = players
		self._hands = {}
		for player in self._players:
			self._hands[player] = []

	def start(self):
		for _ in xrange(NUM_CARDS_IN_HAND):
			for player in self._players:
				self._sendCard(player)
		while not self._isGameEnds():
			for player in self._players:
				self._printGameStatus()
				self._wait()
				action = player.act()		
				if action.act in [ACTION_PLAY, ACTION_DISCARD]:
					self._actRelatedToCard(player, action.act, action.loc)
				self.lastAct = action
				print player.label, action
				if self._isGameEnds():
					break
		self._gameEnds()
	
	def _sendCard(self, player):
		if not self._deck:
			return
		self._hands[player].append(self._deck.pop(0))

	def _actRelatedToCard(self, player, act, loc):
		card = self._hands[player][loc]
		self._hands[player].pop(loc)
		self._sendCard(player)	
		if act == ACTION_PLAY:
			self._play(card)
		elif act == ACTION_DISCARD:
			self._discard(card)
		else:
			raise Error("act not valid")

	def _play(self, card):
		if self.desk[card.color] + 1 == card.number:
			self.desk[card.color] += 1
			return
		self.boom += 1
		self._discard(card)

	def _discard(self, card):
		self.discardedDeck.append(card)

	def _isGameEnds(self):
		if self.boom > BOOM_LIMIT:
			return True	
		hands = self._hands.values()
		if sum([len(h) for h in hands]) == \
			(NUM_CARDS_IN_HAND - ROUND_AFTER_DECK_EMPTY) * len(hands):
			return True
		return False

	def _gameEnds(self):
		self._printGameStatus()
		print "Game Ends with score", self._getScore()

	def _printGameStatus(self):
		print "hands:",
		for player in self._players:
			print [str(card) for card in self._hands[player]],
		print
		desk = ""
		for c in COLOR:
			desk += c + str(self.desk[c]) + " "
		print "desk: ", desk, 
		print "discarded", [str(card) for card in self.discardedDeck],
		print "boom:", self.boom 

	def _getScore(self):
		if self.boom > BOOM_LIMIT:
			return 0
		return sum(self.desk.values())

	def _wait():
    	m.getch()

    def moreTokenExist(self):
    	return self.token > 0

    def isTokenFull(self):
    	return self.token == TOKEN_INIT

    def getHands(self, caller):
    	hands = self._hands.deepcopy()
    	del hands[caller]
    	return hands




