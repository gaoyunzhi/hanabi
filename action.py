from const import COLOR, DECK_DISTRIBUTION, P, D, H

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

	def isActionValid(self):
		if not self.isHint():
			return True
		return len(self.locs) > 0

	def getAllHints():
		return [hint(x) for x in xrange(1, len(DECK_DISTRIBUTION[COLOR[0]]))] + \
			[hint(x) for x in COLOR]

