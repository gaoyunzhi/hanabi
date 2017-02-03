from const import COLOR, DECK_DISTRIBUTION

PLAY = "play"
DISCARD = "discard"
HINT = "hint"
ACT = "act"
LOC = "loc"
LOCS = "locs"


def hint(hint):
	return {
		ACT: HINT,
		HINT: hint,
	}

def play(loc):
	return {
		ACT: PLAY,
		LOC: loc,
	}

def discard(loc):
	return {
		ACT: DISCARD,
		LOC: loc,
	}

def populateLocs(action, hand):
	if action[ACT] != HINT:
		return action
	locs = []
	for index, card in enumerate(hand):
		if action[HINT] in COLOR and card[1] == action[HINT]:
			locs.append(index)
		if (not action[HINT] in COLOR) and int(card[0]) == int(action[HINT]):
			locs.append(index)
	action[LOCS] = locs
	return action

def isHint(action):
	return action[ACT] == HINT

def isPlay(action):
	return action[ACT] == PLAY

def isDiscard(action):
	return action[ACT] == DISCARD

def isActionValid(action):
	if not isHint(action):
		return True
	action = populateLocs(action)
	return len(action[LOCS]) > 0

def getAllHints():
	return [hint(x) for x in xrange(1, len(DECK_DISTRIBUTION[COLOR[0]]))] + \
		[hint(x) for x in COLOR]

