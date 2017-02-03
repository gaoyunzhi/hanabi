from hanabi_player_interface import HanabiPlayerInterface
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from const import COLOR
from public_info import noToken, tokenFull
from state import getInitState, copyState, \
	updateFromOwnAction, updateFromOtherAction, updateFromPublicInfo, \
	getCertainActionFromState, getDiscardAction, getAtomString
from action import isDiscard, getAllHints, isHint

MAX = 10000000

class Player(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label
		self._myState = getInitState()
		self._otherState = getInitState()

	def postAct(self, action, player_index):
		if player_index == 1:
			updateFromOtherAction(self._myState, self._otherState, action, self._judge.publicInfo)
			updateFromOwnAction(self._otherState, action)
		else:
			updateFromOtherAction(self._otherState, self._myState, action, self._judge.publicInfo)
			updateFromOwnAction(self._myState, action)

	def getOthersHand():
		result = []
		for index, card in enumerate(self._judge.getOthersHand()):
			result.append(getAtomString(
				index, self._otherState[STATE][index], self._otherState, card))
		print result


	def act(self):
		self._otherState = updateFromPublicInfo(self._otherState, self._judge.publicInfo)
		self._myState = updateFromPublicInfo(self._myState, self._judge.publicInfo)
		# TODO: integrate private info
		possibilities = set(self.getPossibleActions())
		if not noToken(self._judge.publicInfo):
			possibilities.addAll(getAllHints())
		score = - MAX
		for possibility in possibilities:
			otherState = copyState(self._otherState)
			updateFromOtherAction(otherState, self._myState, possibility, self._judge.publicInfo)
			new_score = scoreState(otherState, self._judge.publicInfo, 
				possibility, self._judge.getOthersHand(self))
			(score, action) = max((score, action), (new_score, possibility))
		return action

	def getPossibleActions(self):
		actions = getCertainActionFromState(self, self._myState)
		if tokenFull(self._judge.publicInfo):
			actions = [action for action in actions if not isDiscard(action)]
		if not actions:
			actions.append(getDiscardAction(self._myState))
		return actions
