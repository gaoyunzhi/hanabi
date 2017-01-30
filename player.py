from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND

class Player(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label
		self._otherDiscardLoc = 0
		self._meDiscardLoc = 0
		self._otherTodo = {}
		self._meTodo = {}
		self._myInfo = {}
		self._otherInfo = {}
		# TODO update info 

	def act(self):
		act = self._act()
		self._meTodo, self._meDiscardLoc = \
			self._updateFromAct(act, self._meTodo, self._meDiscardLoc)
		self._otherTodo, self._otherDiscardLoc = \
			self._updateFromAct(act, self._otherTodo, self._otherDiscardLoc)

	def _act(self):
		self._othersHand = self._getOthersHand()
		self._othersAct = self._judge.lastAct
		self._meTodo, self._meDiscardLoc = \
			self._updateFromHint(self._othersAct, self._meTodo, self._meDiscardLoc)
		self._otherTodo, self._otherDiscardLoc = \
			self._updateFromAct(self._othersAct, self._otherTodo, self._otherDiscardLoc)
		if self._otherSafe() and self._getToPlay(self._meTodo):
			return self._getToPlay(self._meTodo)
		if self._getToPlay(self._otherTodo) or self._judge.token == 0:
			action = Action()
			action.loc = self._meDiscardLoc
			action.act = ACTION_DISCARD
		if self._getPlayHint(self._othersHand):
			return self._getPlayHint(self._othersHand)
		return self._getDiscardHint(self._othersHand)

	def _updateFromHint(self, act, oldTodo, discardLoc):
		if act.act != ACTION_HINT:
			return
		if act.number != None:
			oldTodo[(act.locs[0] + 1) % NUM_CARDS_IN_HAND] = ACTION_PLAY
		if act.color != None:
			discardLoc = (act.locs[0] + 1) % NUM_CARDS_IN_HAND
		return oldTodo, discardLoc	

	# See if other will discard dangerous cards			
	def _otherSafe(self):
		return True

	def _getToPlay(self, todoList):
		for loc, todo in todoList:
			if todo == ACTION_PLAY:
				action = Action()
				action.act = ACTION_PLAY
				action.loc = loc
				return action

	def _updateFromAct(self, act, oldTodo, oldLoc):
		return [self._updateTodoFromAct(act, oldTodo), 
				self._updateDiscardLocFromAct(act, oldLoc)]

	def _updateDiscardLocFromAct(self, act, oldLoc):
		if act.loc == None:
			return oldLoc
		if act.loc < oldLoc:
			return oldLoc - 1
		return oldLoc

	def _updateTodoFromAct(self, act, todoList):
		if act.loc == None:
			return
		newTodoList = {}
		for oldLoc, todo in todoList:
			if oldLoc == act.loc:
				continue
			if oldLoc < act.loc:
				newLoc = oldLoc
			else:
				newLoc = oldLoc - 1
			newTodoList[newLoc] = todo
		return newTodoList

	def _getOthersHand(self):
		return self._judge.getHands(self).values()[0]

	def _canPlay(self, card):
		for c, number in self._judge.desk:
			if card.color == c and card.number == number + 1:	
				return True

	def _getPlayHint(self, hand):
		for index, card in enumerate(hand):
			if self._canPlay(card):
				action = Action()
				action.act = ACTION_HINT
				action.number = \
					hand[(index - 1 + NUM_CARDS_IN_HAND) % NUM_CARDS_IN_HAND].number
				# TODO: deal with ambigious hints later
				return action

	def _getDiscardHint(self, hand):
		discardAvg = avg([self._canDiscard(card) for card in hand])

		for index, card in enumerate(hand):
			if self._canDiscard(card) > discardAvg - 0.000001: # precision
				action = Action()
				action.act = ACTION_HINT
				action.color = \
					hand[(index - 1 + NUM_CARDS_IN_HAND) % NUM_CARDS_IN_HAND].color
				# TODO: deal with ambigious hints later
				return action

	# return a rating from 0 to 1
	def _canDiscard(self, card):
		for c, number in self._judge.desk:
			if card.color == c and card.number <= number:	
				return 1
		for c, number in self._judge.desk:
			if card.color == c and card.number == number + 1:	
				return 0.2
		if self._judge.discardedDeck[card] + 1 == 
			DECK_DISTRIBUTION[card.color][card.number]:
			# last card
			return 0.2
		return 0.5

		