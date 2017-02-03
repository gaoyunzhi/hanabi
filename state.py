from const import NUM_CARDS_IN_HAND
from action import LOCS, HINT, hint, play, discard, isHint
from public_info import ROUND

MARK = "mark"
STATE = "state"
POS_INFO = "pos_info"
NEG_INFO = "neg_info"
ROUND_GET = "round_get"
DISCARD_LOC = "discard_loc"
HINT_LOC = "hint_loc"

P = "to play"
K = "to keep"
D = "to discard"

def getInitState():
	return {
		STATE: atom(-1) for _ in xrange(NUM_CARDS_IN_HAND),
		DISCARD_LOC: 0,
		HINT_LOC: 4
	}

def getInitAtom(round):
	atom = {}
	atom[MARK] = [P, K, D]
	atom[POS_INFO] = set()
	atom[NEG_INFO] = set()
	atom[ROUND_GET] = round
	return atom

def _copyAtom(atom):
	return {
		MARK: list(atom[MARK]),
		POS_INFO: set(atom[POS_INFO]),
		NEG_INFO: set(atom[NEG_INFO]),
		ROUND_GET: atom[ROUND_GET]
	}

def copyState(state):
	return {
		STATE: [_copyAtom(a) for a in state[STATE]]
		DISCARD_LOC: state[DISCARD_LOC],
		HINT_LOC: state[STATE][HINT_LOC]
	}

def _updateFromHint(state, action, public_info):
	for index, atom in enumerate(state[STATE]):
		if index in action[LOCS]:
			atom.POS_INFO.add(action[HINT])
		else:
			atom.NEG_INFO.add(action[HINT])
	updateFromPublicInfo(state, public_info)

def updateFromOwnAction(state, action):
	if action[LOC] != None:
		state[STATE].pop(action[LOC])

def updateFromOtherAction(state, others_state, action, public_info):
	updateFromPublicInfo(state, public_info)
	updateFromPublicInfo(others_state, public_info)
	if not isHint(action):
		possiblities = getCertainActionFromState(others_state)
		index = [a[LOC] for a in possiblities].index(action[LOC])
		if index == -1:
			raise Exception("bug in update other's action")
		for _ in xrange(index):
			if state[STATE][state[HINT_LOC]][MARK] == [K, P]:
				state[STATE][state[HINT_LOC]][MARK] = [K]
			state[STATE][state[HINT_LOC]][MARK].remove(D)
			state[HINT_LOC] = _findNextHintLoc(state)
		if index !== len(possiblities):
			if state[STATE][state[HINT_LOC]][MARK] == [K, P]:
				state[STATE][state[HINT_LOC]][MARK] = [P]
			else:
				state[STATE][state[HINT_LOC]][MARK] = [D]
		state[HINT_LOC] = _findNextHintLoc(state)
		return
	_updateFromHint(state, action, public_info)
	if not action[HINT] in COLOR:
		_updateFromNumberHint(state, action, public_info)
	else:
		_updateFromColorHint(state, action, public_info)
	updateFromPublicInfo(state, public_info)

def _updateFromColorHint(state, action, public_info):
	num = len(state[STATE])
	for offset in _xrange(num):
		for loc in action[LOCS]:
			discard_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
			if state[STATE][discard_loc][MARK].index(D) != -1:
				state[DISCARD_LOC] = discard_loc
				return
	print "reach end of _updateFromColorHint"
	state[DISCARD_LOC] = discard_loc

def _updateFromNumberHint(state, action, public_info):
	num = len(state[STATE])
	for offset in _xrange(num):
		for loc in action[LOCS]:
			play_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
			if state[STATE][play_loc][MARK].index(P) != -1:
				state[STATE][play_loc][MARK] = [P]
				return
	print "reach end of _updateFromNumberHint"
	state[STATE][play_loc][MARK] = [P]
			
def _findNextHintLoc(state):
	num = len(state[STATE])
	hint_loc = state[HINT_LOC]
	for _ in xrange(num - 1):
		hint_loc = (hint_loc + num - 1) % num
		if state[STATE][hint_loc][MARK].index(D) != -1 and \
			state[STATE][hint_loc][MARK] != [D]:
			return hint_loc
	return hint_loc

def _findNextDiscardLoc(state):
	num = len(state[STATE])
	for offset in xrange(num + 1):
		discard_loc = (state[DISCARD_LOC] + offset) % num
		if state[STATE][discard_loc][MARK].index(D) != -1:
			return discard_loc
	return discard_loc

def updateFromPublicInfo(state, public_info):
	if state[STATE][state[HINT_LOC]][MARK].index(D) == -1 or \
		state[STATE][state[HINT_LOC]][MARK] == [D]:
		state[HINT_LOC] -= 1
		state[HINT_LOC] = _findNextHintLoc(state)
	state[DISCARD_LOC] = _findNextDiscardLoc(state)

def getCertainActionFromState(state):
	res = []
	for index, atom in enumerate(state):
		if atom[MARK] == [P]:
			res.append(play(index))
		elif atom[MARK] == [D]:
			res.append(discard(index))
	return res

def getDiscardAction(state):
	return discard(state[DISCARD_LOC])


