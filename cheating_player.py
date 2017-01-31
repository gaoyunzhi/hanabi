from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from card import Card
from const import MULTI_COLOR

class CheatingPlayer(HanabiPlayerInterface):
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label

	def setOther(self, other):
		self._other = other

	def act(self):
		self._otherHand = self._judge.getHands(self).values()[0]
		self._myHand = self._judge.getHands(self._other).values()[0]
	
		if self._getPotentialPlayAction(self._myHand, self._otherHand):
			return self._getPotentialPlayAction(self._myHand, self._otherHand)
		if self._judge.isTokenFull():
			return self._getHintAction()

		if self._judge.getScore() < 17 and self._getPotentialDiscardAction(self._myHand, self._otherHand):
			return self._getPotentialDiscardAction(self._myHand, self._otherHand)	

		if self._judge.token > 0 and self._judge.lastAct.act != ACTION_HINT:
			return self._getHintAction()
		if self._getPotentialDiscardAction(self._myHand, self._otherHand):
			return self._getPotentialDiscardAction(self._myHand, self._otherHand)

		if self._judge.token == 0:
			return self._getBestDiscardAction(self._myHand)

		if self._hasValidThingTodo(self._otherHand, self._myHand):
			return self._getHintAction()
		if max([self._discardScore(c) for c in self._myHand]) < \
			min(0.3, max([self._discardScore(c) for c in self._otherHand]) - 0.000001):
			return self._getHintAction()
		return self._getBestDiscardAction(self._myHand)

	def _hasValidThingTodo(self, hand, otherHand):
		if self._getPotentialPlayAction(hand, otherHand):
			return True
		if self._getPotentialDiscardAction(hand, otherHand):
			return True
		return False

	def _getBestDiscardAction(self, hand):
		max_score = max([self._discardScore(c) for c in hand])
		for index, card in enumerate(hand):
			if self._discardScore(card) > max_score - 0.00001:
				action = Action()
				action.act = ACTION_DISCARD
				action.loc = index
				return action

	def _getPotentialPlayAction(self, hand, otherHand):
		for index, card in enumerate(hand):
			if not self._canPlay(card):
				continue
			if self._blockOther(card, otherHand):
				action = Action()
				action.act = ACTION_PLAY
				action.loc = index
				return action
		for index, card in enumerate(hand):
			if self._canPlay(card):
				action = Action()
				action.act = ACTION_PLAY
				action.loc = index
				return action

	def _blockOther(self, card, otherHand):
		if str(card) in [str(c) for c in otherHand]:
			return True
		cardNext = Card(card.number + 1, card.color)
		if str(card) in [str(c) for c in otherHand]:
			return True

	def _getPotentialDiscardAction(self, hand, otherHand):
		for index, card in enumerate(hand):
			if self._canDiscard(card, hand, otherHand):
				action = Action()
				action.act = ACTION_DISCARD
				action.loc = index
				return action

	def _getHintAction(self):
		action = Action()
		action.act = ACTION_HINT
		action.number = self._otherHand[0].number
		return action

	def _canDiscard(self, card, hand, otherHand):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number <= number:	
				return True	
		if sum([str(c) == str(card) for c in hand]) > 1:
			return True
		if self._isNoHope(card):
			return True
		return False

	def _isNoHope(self, card):
		# number = card.number - 1
		# while number > 0:
		# 	if self._judge.discardedDeck.get(str(number) + card.color, 0) == \
		# 		DECK_DISTRIBUTION[card.color][number]:
		# 		return True
		# 	number -= 1
		return False

	def _discardScore(self, card):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number <= number:	
				return 1.0
		if self._isNoHope(card):
			return 1.0
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number == number + 1:	
				return 0.0
		if sum([str(c) == str(card) for c in self._otherHand]) > 0:
			return 0.8
		if self._judge.discardedDeck.get(str(card), 0) + 1 == \
			DECK_DISTRIBUTION[card.color][card.number]:
			# last card
			return 0.2 + [1, 2, 3, 4, 5, 6][card.number] * 0.045
		# allCards = self._getAllCards()
		# number = self._judge.desk[card.color] + 1
		# score = 0.3
		# while number < card.number:
		# 	waiting_card = Card(number, card.color)
		# 	if not str(waiting_card) in allCards:
		# 		score += 0.1
		# 	number += 1
		# return score
		return [0.3, 0.4, 0.5, 0.6, 0.7][card.number]

	def _getAllCards(self):
		result = set()
		for card in self._myHand + self._otherHand:
			result.add(str(card))
		return result

	def _canPlay(self, card):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number == number + 1:	
				return True

		