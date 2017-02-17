from const import COLOR, DECK_DISTRIBUTION

PLAY = "play"
DISCARD = "discard"
HINT = "hint"

class Action(object):
	def __init__(self):
		self.act = None
		self.loc = None

	def hint(hint):
		self.act = HINT
		self.hint = hint

	def play(loc):
		self.act = PLAY
		self.loc = loc

	def discard(loc):
		self.act = DISCARD
		self.loc = loc

	def populateLocs(action, hand):
		if action.act != HINT:
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
		return self.act == HINT

	def isPlay(self):
		return self.act == PLAY

	def isDiscard(self):
		return self.act == DISCARD

	def isActionValid(self):
		if not self.isHint():
			return True
		return len(self.locs) > 0

	def getAllHints():
		return [hint(x) for x in xrange(1, len(DECK_DISTRIBUTION[COLOR[0]]))] + \
			[hint(x) for x in COLOR]

