from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from const import COLOR

class SmartPlayer(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label
		self._myState = SmartState()
		self._otherState = SmartState()

	def postAct(self, action, actionResult):
		if action in [ACTION_PLAY, ACTION_DISCARD]:
			self._myState.updateFromActionResult(actionResult)
			self._otherState.updateFromActionResult(actionResult)
			# deal with boom?

	def act(self):
		action = self._act()
		self.populateLocs(action)
		self._myState.updateFromAction(action)
		self._otherState.updateFromHint(action)
		return action

	def populateLocs(self, action):
		self._judge.populateLocs(action, self)

	def _act(self):
		if (not (self._otherState.isDangerous() and self._judge.token > 0)) and \
			self._myState.getPlayAction():
			return self._myState.getPlayAction()
		if self._judge.token > 0 and self._otherState.hasNothingToPlay() and \
			self._otherState.getPlayHint(self._getOthersHand()):
			return self._otherState.getPlayHint(self._getOthersHand())
		if (self._otherState.isPotentiallyDangerous() and self._judge.token > 0) or self._judge.isTokenFull():
			return self._otherState.getDiscardHint(self._getOthersHand())
		return self._myState.getDiscardAction():

	def getCanPlaySet(self):
		can_play = set()
		for c, number in self._judge.desk.iteritems():
			if len(DECK_DISTRIBUTION[c]) > number + 1:
				canPlay.add(str(number + 1), c)
		return can_play

	def getInitPossibleCards(self):
		cards = {}
		for c in COLOR:
			for n, count in DECK_DISTRIBUTION[c]:
				if count > 0:
					cards[str(n) + c] = count
		return cards

	def getSeenCards(self):
		discardedDeck = []
		for card, number in self._judge.discardedDeck.iteritems():
			discardedDeck.append([card] * number)
		return self._getOthersHand() + discardedDeck + self.getDesk()

	def getDesk(self):
		desk = []
		for c, number in self._judge.desk.iteritems():
			for n in xrange(1, number + 1):
				desk.append(Card(n, c))
		return desk

	def _getOthersHand(self):
		return self._judge.getHands(self).values()[0]


		