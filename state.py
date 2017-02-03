from const import NUM_CARDS_IN_HAND, DECK_DISTRIBUTION
from action import LOCS, HINT, hint, play, discard, isHint
from public_info import ROUND, getPlayableCards, getDiscardableCards, 
	getUndiscardbleCards, getSuggestDiscardCards, getPossibleHandCards

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
	atom[MARK] = set([P, K, D])
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
			if state[STATE][state[HINT_LOC]][MARK] == set([K, P]):
				state[STATE][state[HINT_LOC]][MARK] = set([K])
			state[STATE][state[HINT_LOC]][MARK].remove(D)
			state[HINT_LOC] = _findNextHintLoc(state)
		if index !== len(possiblities):
			if state[STATE][state[HINT_LOC]][MARK] == set([K, P]):
				state[STATE][state[HINT_LOC]][MARK] = set([P])
			else:
				state[STATE][state[HINT_LOC]][MARK] = set([D])
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
			if D in state[STATE][discard_loc][MARK]:
				state[DISCARD_LOC] = discard_loc
				return
	print "reach end of _updateFromColorHint"
	state[DISCARD_LOC] = discard_loc

def _updateFromNumberHint(state, action, public_info):
	num = len(state[STATE])
	for offset in _xrange(num):
		for loc in action[LOCS]:
			play_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
			if P in state[STATE][play_loc][MARK]:
				state[STATE][play_loc][MARK] = set([P])
				return
	print "reach end of _updateFromNumberHint"
	state[STATE][play_loc][MARK] = set([P])
			
def _findNextHintLoc(state):
	num = len(state[STATE])
	hint_loc = state[HINT_LOC]
	for _ in xrange(num - 1):
		hint_loc = (hint_loc + num - 1) % num
		if D in state[STATE][hint_loc][MARK] and \
			state[STATE][hint_loc][MARK] != set([D]):
			return hint_loc
	return hint_loc

def _findNextDiscardLoc(state):
	num = len(state[STATE])
	for offset in xrange(num + 1):
		discard_loc = (state[DISCARD_LOC] + offset) % num
		if D in state[STATE][discard_loc][MARK]:
			return discard_loc
	return discard_loc

def updateFromPublicInfo(state, public_info):
	p, d, k, s, a = getPlayableCards(public_info), getDiscardableCards(public_info), 
		getUndiscardbleCards(public_info), getSuggestDiscardCards(public_info),
		getPossibleHandCards(public_info)
	for atom in state[STATE]:
		_updateAtom(atom, p, d, k, s, a)
	if public_info[NUM_CARDS_IN_DECK] > 0 and len(state[STATE]) < NUM_CARDS_IN_HAND:
		state[STATE].add(getInitAtom(public_info[ROUND]))
	if (not D in state[STATE][state[HINT_LOC]][MARK]) or \
		state[STATE][state[HINT_LOC]][MARK] == set([D]):
		state[HINT_LOC] -= 1
		state[HINT_LOC] = _findNextHintLoc(state)
	state[DISCARD_LOC] = _findNextDiscardLoc(state)

def _updateAtom(atom, p, d, k, s, a):
	colors = set(COLOR)
	if atom[POS] & colors:
		colors = atom[POS] & colors
	else:
		colors -= atom[NEG]
	numbers = set(xrange(1, len(DECK_DISTRIBUTION[COLOR[0]])))
	if atom[POS] & numbers:
		numbers = atom[POS] & numbers
	else:
		numbers -= atom[NEG]
	possibleSet = set()
	for c in colors:
		for num in numbes:
			possibleSet.add(str(num) + c)
	possibleSet &= a
	if not possibleSet & p:
		atom[MARK] -= P
	if not possibleSet & (d + s):
		atom[MARK] -= D
	# if not possibleSet & k:
	# 	atom[MARK] -= K

def getCertainActionFromState(state):
	res = []
	for index, atom in enumerate(state):
		if atom[MARK] == set([P]):
			res.append(play(index))
		elif atom[MARK] == set([D]):
			res.append(discard(index))
	return res

def getDiscardAction(state):
	return discard(state[DISCARD_LOC])

def scoreState(state, public_info, action, hand):
	p, d, k, s = getPlayableCards(public_info), getDiscardableCards(public_info), 
		getUndiscardbleCards(public_info), getSuggestDiscardCards(public_info)
	score = 0
	num_certain_actions = len(getCertainActionFromState(state))
	for index, atom in enumerate(state[STATE]):
		if atom == [P] and not hand[index] in p:
			score -= BOOM_PENALTY / (BOOM_LIMIT - public_info[BOOM] + 0.001) / num_certain_actions


