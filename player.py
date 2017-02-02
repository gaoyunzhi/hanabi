from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from const import COLOR
from card import Card
from smart_state import SmartState

class JanPlayer(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label

	def postAct(self, action, actionResult, player_index):
		if action.act in [ACTION_PLAY, ACTION_DISCARD]:
			self._myState.updateFromPostActionWithCard(action, actionResult)
			self._otherState.updateFromPostActionWithCard(action, actionResult)
			if player_index == 1:
				self._otherState.updateOwnAction(action, actionResult)
			else:
				self._myState.updateOwnAction(action, actionResult)
			# deal with boom?
		if action.act == ACTION_HINT:
			if player_index == 1:
				self._myState.updateFromHint(action)
			else:
				if player_index != 0:
					raise Exception("only support two players")
				self._otherState.updateFromHint(action)

	def populateLocs(self, action):
		self._judge.populateLocs(action, self)

	def act(self):
		if (not (self._otherState.isDangerous(self._getOthersHand()) and self._judge.token > 0)) and \
			self._myState.getPlayAction():
			return self._myState.getPlayAction()
		if self._judge.token > 0 and (not self._otherState.getPlayAction()) and \
			self.getPlayHint():
			return self.getPlayHint()
		if (self._otherState.isPotentiallyDangerous(self._getOthersHand()) and self._judge.token > 0) and self.getDiscardHint():
			return self.getDiscardHint()
		if self._judge.isTokenFull():
			return self.getDiscardHint() or self.defaultHint()
		
		return self._myState.getDiscardAction()

	def getPlayHint(self):
		hand = self._getOthersHand()
		if len(hand) < NUM_CARDS_IN_HAND:
			return None
		bestAction = None
		bestScore = 0
		for card in hand:
			action = Action()
			action.number = card.number
			action.act = ACTION_HINT
			self._judge.populateLocs(action, self)
			toPlay, certainPlays = self._otherState.getPlayResultFromHint(action)
			if toPlay == None or not (str(hand[toPlay]) in self.getCanPlaySet()):
				continue
			plays = set(certainPlays)
			plays.add(toPlay)
			score = len(plays)
			if score > bestScore:
				bestScore = score
				bestAction = action
		return bestAction

	def defaultHint(self):
		action = Action()
		action.act = ACTION_HINT
		action.color = self._getOthersHand()[0].color
		return action	

	def getDiscardHint(self):
		hand = self._getOthersHand()
		bestAction = None
		bestScore = -1
		for card in hand:
			action = Action()
			action.color = card.color
			action.act = ACTION_HINT
			self._judge.populateLocs(action, self)
			newDiscardLoc, certainDiscards, certainPlays = \
				self._otherState.getDiscardResultFromHint(action)
			score = len(set(certainPlays)) * 5 + len(set(certainDiscards))
			if len(set(certainPlays)) == 0 and len(set(certainDiscards)) == 0:
				if str(hand[newDiscardLoc]) in self.getDangerousSet():
					continue
			if score > bestScore:
				bestScore = score
				bestAction = action 
		return bestAction

	def getCanPlaySet(self):
		can_play = set()
		for c, number in self._judge.desk.iteritems():
			if len(DECK_DISTRIBUTION[c]) > number + 1:
				can_play.add(str(number + 1) + c)
		return can_play

	def getInitPossibleCards(self):
		cards = {}
		for c in COLOR:
			for n, count in enumerate(DECK_DISTRIBUTION[c]):
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
				desk.append(str(Card(n, c)))
		return desk

	def getDangerousSet(self):
		res = set()
		for c in COLOR:
			for n in xrange(self._judge.desk[c] + 1, len(DECK_DISTRIBUTION[c])):
				if self._judge.discardedDeck.get(str(n) + c, 0) + 1 == \
					DECK_DISTRIBUTION[c][n]:
					res.add(str(n) + c)
				if self._judge.discardedDeck.get(str(n) + c, 0) == DECK_DISTRIBUTION[c][n]:
					break
		return res

	def _getOthersHand(self):
		return self._judge.getHands(self).values()[0]

	def hasMoreCardsInDeck(self):
		return self._judge.isPlayerHandsFull()


		