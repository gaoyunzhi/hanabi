from hanabi_player_interface import HanabiPlayerInterface
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from const import COLOR
from public_info import noToken, tokenFull
from state import getInitState, copyState, \
	updateFromOwnAction, updateFromOtherAction, updateFromPublicInfo, \
	getCertainActionFromState, getDiscardAction, getAtomString, scoreState, STATE
from action import isDiscard, getAllHints, isHint, populateLocs, LOCS

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

	def getOthersHand(self):
		return self._getOtherHand(self._otherState)

	def _getOtherHand(self, original_state):
		result = []
		state = copyState(original_state)
		updateFromPublicInfo(state, self._judge.publicInfo)
		for index, card in enumerate(self._judge.getOthersHand(self)):
			result.append(getAtomString(index, state[STATE][index], state, card))
		return result

	def act(self):
		updateFromPublicInfo(self._otherState, self._judge.publicInfo)
		updateFromPublicInfo(self._myState, self._judge.publicInfo)
		# TODO: integrate private info
		possibilities = self.getPossibleActions()
		if not noToken(self._judge.publicInfo):
			possibilities += getAllHints()
		score = - MAX
		action = None
		for possibility in possibilities:
			possibility = populateLocs(possibility, self._judge.getOthersHand(self))
			if isHint(possibility) and len(possibility[LOCS]) == 0:
				continue
			otherState = copyState(self._otherState)
			updateFromOtherAction(otherState, self._myState, possibility, self._judge.publicInfo)
			new_score = scoreState(otherState, self._myState, self._judge.publicInfo, 
				possibility, self._judge.getOthersHand(self))
			# print new_score, possibility, self._getOtherHand(otherState)
			(score, action) = max((score, action), (new_score, possibility))
		return action

	def getPossibleActions(self):
		actions = getCertainActionFromState(self._myState)
		if tokenFull(self._judge.publicInfo):
			actions = [action for action in actions if not isDiscard(action)]
		elif not actions:
			actions.append(getDiscardAction(self._myState))
		return actions
