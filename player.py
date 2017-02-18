from hanabi_player_interface import HanabiPlayerInterface
from const import DECK_DISTRIBUTION, NUM_CARDS_IN_HAND, COLOR, P, D
from action import Action

class Player(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label
		self._myState = getInitState()
		self._otherState = getInitState()

	def postAct(self, action, player_index):
		if player_index == 0:
			self._otherState.updateFromOtherAction(self._myState, action, self._judge.publicInfo)
			self._myState.updateFromOwnAction(action)
		else:
			self._myState.updateFromOtherAction(self._otherState, action, self._judge.publicInfo)
			self._otherState.updateFromOwnAction(action)

	def getOthersHand(self):
		result = []
		state = self._otherState.copy()
		state.updateFromPublicInfo(self._judge.publicInfo)
		for index, card in enumerate(self._judge.getOthersHand(self)):
			result.append(state.cards[index].getString(card))
		return result

	def act(self):
		self._otherState.updateFromPublicInfo(self._judge.publicInfo)
		self._myState.updateFromPublicInfo(self._judge.publicInfo)
		if self._judge.publicInfo.token == 0 and self.getMyPlay():
			return self.getMyActionWithScore()[0]
		# token > 0
		if self.getPlayHint():
			return self.getPlayHint()
		score1, colorHint = self.getColorHintWithScore()
		score2, myAction = self.getMyActionWithScore()
		if score1 > score2:
			return colorHint
		else:
			return myAction

	def getPlayHint(self):
		if not set(otherhand) & p:
			return None
		base_line = self._otherState.getPlayScore(self._judge.publicInfo, self._myState, hand)
		otherhand = self._judge.getOthersHand(self)
		res = []
		for i in xrange(1, len(DECK_DISTRIBUTION[COLOR[0]])):
			action = Action.hint(i)
			action.populateLocs(otherhand)
			if not action.locs:
				continue
			new_state = self._otherState.copy()
			new_state.updateFromOtherAction(self._myState, action, self._judge.publicInfo)
			new_score = new_state.getPlayScore(self._judge.publicInfo, self._myState, hand) + \
				new_state.getStateAdjuestScore(self._judge.publicInfo, self._otherState, hand)
			if new_score >= 0.6 + base_line:
				res.append((new_score, action))
		if not res:
			return None
		return max(res)[1]

	def getMyActionWithScore(self):
		base_line = self._otherState.getDiscardScore(self._judge.publicInfo, self._myState, hand)
		actions = self.getPossibleActions()
		if not actions:
			return None, -10 # token full
		res = []
		for a, loc in actions:
			action = Action()
			action.act = a
			action.loc = loc
			new_state = self._otherState.copy()
			new_state.updateFromOtherAction(self._myState, action, self._judge.publicInfo)
			new_score = new_state.getDiscardScore(self._judge.publicInfo, self._myState, hand) - \
				action.getDiscardPenalty(self._judge.publicInfo, oh)
			res.append(new_score - baseline + self.state.cards[loc].getActionScore(), action)
		return max(res)

	def getColorHintWithScore(self):
		base_line = self._otherState.getDiscardScore(self._judge.publicInfo, self._myState, hand)
		otherhand = self._judge.getOthersHand(self)
		res = []
		for i in xrange(1, COLOR):
			action = Action.hint(i)
			action.populateLocs(otherhand)
			if not action.locs:
				continue
			new_state = self._otherState.copy()
			new_state = self._otherState.updateFromOtherAction(self._myState, action, self._judge.publicInfo)
			new_score = new_state.getDiscardScore(self._judge.publicInfo, self._myState, hand) + \
				new_state.getStateAdjuestScore(self._judge.publicInfo, self._myState, self._otherState, hand)
			res.append((new_score - baseline, action))
		return max(res)

	def getPossibleActions(self, meHint=False):
		actions = self._myState.getCertainActionPrivate(
			self._judge.publicInfo, self._otherState, self._judge.getOthersHand(self))
		if self._judge.publicInfo.tokenFull() and not meHint:
			actions = [action for action in actions if not action[0] == D]		
		return actions
