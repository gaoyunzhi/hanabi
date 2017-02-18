from const import COLOR, DECK_DISTRIBUTION, P, D, H, ROUND_AFTER_DECK_EMPTY

class Action(object):
	def __init__(self):
		self.act = None
		self.loc = None

	def hint(hint):
		self.act = H
		self.hint = hint

	def play(loc):
		self.act = P
		self.loc = loc

	def discard(loc):
		self.act = D
		self.loc = loc

	def populateLocs(action, hand):
		if action.act != H:
			return action
		locs = []
		for index, card in enumerate(hand):
			if action.hint in COLOR and card[1] == action.hint:
				locs.append(index)
			if (not action.hint in COLOR) and int(card[0]) == int(action.hint):
				locs.append(index)
		action.locs = locs
		return action

	def isHint(self):
		return self.act == H

	def isPlay(self):
		return self.act == P

	def isDiscard(self):
		return self.act == D

	def isValid(self):
		if not self.isHint():
			return True
		return len(self.locs) > 0

	def getDiscardPenalty(self, public_info, oh):
		if not self.isDiscard():
			return 0
		p, d, k, s, a = public_info.getSuggestedSets()
		if not set(oh) & p:
			return 0
		round_can_discard = public_info.num_cards_in_deck + ROUND_AFTER_DECK_EMPTY * public_info.num_player \
			- public_info.act_after_empty - len(a - d)
		if round_can_discard < 0:
			return -1
		if round_can_discard > 3:
			return 0
		return [0.2, 0.3, 0.4][round_can_discard]



