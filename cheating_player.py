from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from card import Card

class CheatingPlayer(HanabiPlayerInterface):
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label

	def setOther(self, other):
		self._other = other

	def act(self):
		self._otherHand = self._judge.getHands(self).values()[0]
		self._myHand = self._judge.getHands(self._other).values()[0]
	
		if self._getPotentialPlayAction():
			return self._getPotentialPlayAction()
		if self._judge.isTokenFull():
			return self._getHintAction()

		if self._judge.getScore() < 20 and self._getPotentialDiscardAction():
			return self._getPotentialDiscardAction()		

		if self._judge.token > 0 and self._judge.lastAct.act != ACTION_HINT:
			return self._getHintAction()
		if self._judge.token == 0 and self._getPotentialDiscardAction():
			return self._getPotentialDiscardAction()

		return self._getBestDiscardAction()

	def _getBestDiscardAction(self):
		maxScroe = max([self._discardScore(c) for c in self._myHand])
		for index, card in enumerate(self._myHand):
			if self._discardScore(card) > maxScroe - 0.00001:
				action = Action()
				action.act = ACTION_DISCARD
				action.loc = index
				return action

	def _getPotentialPlayAction(self):
		for index, card in enumerate(self._myHand):
			if not self._canPlay(card):
				continue
			if self._blockOther(card):
				action = Action()
				action.act = ACTION_PLAY
				action.loc = index
				return action
		for index, card in enumerate(self._myHand):
			if self._canPlay(card):
				action = Action()
				action.act = ACTION_PLAY
				action.loc = index
				return action

	def _blockOther(self, card):
		if str(card) in [str(c) for c in self._otherHand]:
			return True
		cardNext = Card(card.number + 1, card.color)
		if str(card) in [str(c) for c in self._otherHand]:
			return True

	def _getPotentialDiscardAction(self):
		for index, card in enumerate(self._myHand):
			if self._canDiscard(card):
				action = Action()
				action.act = ACTION_DISCARD
				action.loc = index
				return action

	def _getHintAction(self):
		action = Action()
		action.act = ACTION_HINT
		action.number = self._otherHand[0].number
		return action

	def _canDiscard(self, card):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number <= number:	
				return True	
		if sum([str(c) == str(card) for c in self._myHand]) > 1:
			return True
		return False

	def _discardScore(self, card):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number <= number:	
				return 1.0
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number == number + 1:	
				return 0.0
		if sum([str(c) == str(card) for c in self._otherHand]) > 0:
			return 0.8
		if self._judge.discardedDeck.get(str(card), 0) + 1 == \
			DECK_DISTRIBUTION[card.color][card.number]:
			# last card
			return 0.2
		allCards = self._getAllCards()
		number = self._judge.desk[card.color] + 1
		score = 0.3
		while number < card.number:
			waiting_card = Card(number, card.color)
			if not str(waiting_card) in allCards:
				score += 0.1
			number += 1
		return score

	def _getAllCards(self):
		result = set()
		for card in self._myHand + self._otherHand:
			result.add(str(card))
		return result

	def _canPlay(self, card):
		for c, number in self._judge.desk.iteritems():
			if card.color == c and card.number == number + 1:	
				return True

		