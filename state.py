from const import NUM_CARDS_IN_HAND, DECK_DISTRIBUTION, COLOR, MARK, POS, NEG, P, K, D, PKD
from action import LOCS, LOC, HINT, hint, play, discard, isHint, isDiscard
from public_info import ROUND, BOOM, getPlayableCards, getDiscardableCards, \
	getUndiscardbleCards, getSuggestDiscardCards, getPossibleHandCards, NUM_CARDS_IN_DECK, ACT_AFTER_EMPTY
from scoring import boomScore, failureScore, numActionScore, wrongMark, \
	keepScore, blockedSpaceScore, discardScore, tokenMinus, tokenAdd, knowledgeScore, discardPenalty, playMarkScore, \
	discardMarkScore

STATE = "state"
ROUND_GET = "round_get"
DISCARD_LOC = "discard_loc"
HINT_LOC = "hint_loc"

def getInitState():
	return {
		STATE: [getInitAtom(-1) for _ in xrange(NUM_CARDS_IN_HAND)],
		DISCARD_LOC: 0,
		HINT_LOC: 4
	}

def getInitAtom(round):
	atom = {}
	atom[MARK] = set([P, K, D])
	atom[POS] = set()
	atom[NEG] = set()
	atom[ROUND_GET] = round
	return atom

def _copyAtom(atom):
	return {
		MARK: set(atom[MARK]),
		POS: set(atom[POS]),
		NEG: set(atom[NEG]),
		ROUND_GET: atom[ROUND_GET]
	}

def _toCard(atom, a):
	possibleSet = _getPossibleSet(atom, a)
	if len(possibleSet) == 1:
		return next(iter(possibleSet))
	return None

def getAtomString(index, atom, state, card):
	result = card[:]
	if len(atom[POS]) == 1:
		if next(iter(atom[POS])) in COLOR:
			result = card[0] + '[' + card[1] + ']'
		else:
			result = '[' + card[0] + ']' + card[1]
	elif len(atom[POS]) == 2:
		result = '[' + card + ']'
	if not len(atom[MARK]) == 3:
		result += '.' + ''.join([PKD[m] for m in atom[MARK]])
	if index == state[DISCARD_LOC]:
		result += '.d'
	if index == state[HINT_LOC]:
		result += '.h'
	return result

def copyState(state):
	return {
		STATE: [_copyAtom(a) for a in state[STATE]],
		DISCARD_LOC: state[DISCARD_LOC],
		HINT_LOC: state[HINT_LOC]
	}

def _updateFromHint(state, action, public_info):
	for index, atom in enumerate(state[STATE]):
		if index in action[LOCS]:
			atom[POS].add(action[HINT])
		else:
			atom[NEG].add(action[HINT])
	updateFromPublicInfo(state, public_info)

def updateFromOwnAction(state, action):
	if LOC in action and action[LOC] != None:
		state[STATE].pop(action[LOC])
		if state[DISCARD_LOC] > action[LOC]:
			state[DISCARD_LOC] -= 1

def updateFromOtherAction(state, others_state, action, public_info):
	updateFromPublicInfo(state, public_info)
	updateFromPublicInfo(others_state, public_info)
	if not isHint(action):
		possiblities = getCertainActionFromState(others_state)
		if not action[LOC] in [a[LOC] for a in possiblities]:
			return
		index = [a[LOC] for a in possiblities].index(action[LOC])
		for _ in xrange(index):
			if state[STATE][state[HINT_LOC]][MARK] == set([K, D]):
				state[STATE][state[HINT_LOC]][MARK] = set([K])
			if not state[STATE][state[HINT_LOC]][MARK] == set([P]):
				state[STATE][state[HINT_LOC]][MARK].discard(P)
			state[HINT_LOC] = _findNextHintLoc(state)
		if index != len(possiblities) - 1:
			if state[STATE][state[HINT_LOC]][MARK] == set([K, D]):
				state[STATE][state[HINT_LOC]][MARK] = set([D])
			else:
				state[STATE][state[HINT_LOC]][MARK] = set([P])
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
	for offset in xrange(num):
		for loc in action[LOCS]:
			discard_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
			if D in state[STATE][discard_loc][MARK]:
				state[DISCARD_LOC] = discard_loc
				return
	state[DISCARD_LOC] = discard_loc

def _updateFromNumberHint(state, action, public_info):
	num = len(state[STATE])
	for offset in xrange(num):
		for loc in action[LOCS]:
			play_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
			if P in state[STATE][play_loc][MARK]:
				state[STATE][play_loc][MARK] = set([P])
				return
	state[STATE][play_loc][MARK] = set([P])
			
def _findNextHintLoc(state):
	num = len(state[STATE])
	hint_loc = state[HINT_LOC]
	for _ in xrange(num):
		if P in state[STATE][hint_loc][MARK] and state[STATE][hint_loc][MARK] != set([P]):
			return hint_loc
		hint_loc = (hint_loc + num - 1) % num
	return hint_loc

def _findNextDiscardLoc(state):
	num = len(state[STATE])
	for offset in xrange(num + 1):
		discard_loc = (state[DISCARD_LOC] + offset) % num
		if D in state[STATE][discard_loc][MARK]:
			return discard_loc
	return discard_loc

def updateFromPublicInfo(state, public_info):
	[p, d, k, s, a] = [getPlayableCards(public_info), getDiscardableCards(public_info), 
		getUndiscardbleCards(public_info), getSuggestDiscardCards(public_info),
		getPossibleHandCards(public_info)]
	for atom in state[STATE]:
		_updateAtom(atom, p, d, k, s, a)
	if public_info[ACT_AFTER_EMPTY] == 0 and len(state[STATE]) < NUM_CARDS_IN_HAND:
		state[STATE].append(getInitAtom(public_info[ROUND] - 1))
		state[HINT_LOC] = len(state[STATE]) - 1
	if state[HINT_LOC] >= len(state[STATE]):
		state[HINT_LOC] -= 1
	state[HINT_LOC] = _findNextHintLoc(state)
	state[DISCARD_LOC] = _findNextDiscardLoc(state)

def _getPossibleSet(atom, a):
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
		for num in numbers:
			possibleSet.add(str(num) + c)
	possibleSet &= a
	return possibleSet

def _updateAtom(atom, p, d, k, s, a):
	possibleSet = _getPossibleSet(atom, a)
	if not possibleSet & p:
		atom[MARK].discard(P)
	if not possibleSet & (d | s):
		atom[MARK].discard(D)
	if possibleSet <= p:
		atom[MARK] = set([P])
	if possibleSet <= d:
		atom[MARK] = set([D])
	if possibleSet <= k:
		atom[MARK].discard(D)
	if atom[MARK] == set([]):
		atom[MARK] = set([P, K, D])
	# if not possibleSet & k:
	# 	atom[MARK] -= K

def getCertainActionFromState(state):
	res = []
	for index, atom in enumerate(state[STATE]):
		if atom[MARK] == set([P]):
			res.append(play(index))
		elif atom[MARK] == set([D]):
			res.append(discard(index))
	# res.reverse()
	return res

def getDiscardAction(state):
	return discard(state[DISCARD_LOC])

def scoreState(state, myState, public_info, action, hand):
	[p, d, k, s, a] = [getPlayableCards(public_info), getDiscardableCards(public_info), 
		getUndiscardbleCards(public_info), getSuggestDiscardCards(public_info),
		getPossibleHandCards(public_info)]
	num_certain_actions = len(getCertainActionFromState(state))
	blocked_space = 0
	itemized_score = []
	for index, atom in enumerate(state[STATE]):
		if atom[MARK] == set([K]) or atom[MARK] == set([K, P]):
			blocked_space += 1
		sub_score = _getItemizedScore(atom, public_info, hand, index, k, s, p, d, num_certain_actions)
		itemized_score.append(sub_score)
	if num_certain_actions > 0:
		itemized_score.append(numActionScore(num_certain_actions, public_info))
	else:
		itemized_score.append(0)
	itemized_score.append(blockedSpaceScore(blocked_space, public_info))
	if num_certain_actions == 0:
		itemized_score.append(discardScore(state[STATE][state[DISCARD_LOC]], \
			hand[state[DISCARD_LOC]], public_info, k, s, d))
		if isDiscard(action) and _toCard(myState[STATE][action[LOC]], a) == hand[state[DISCARD_LOC]]:
			itemized_score.append(failureScore())
	else:
		itemized_score += [0] * 2
	if isHint(action):
		itemized_score.append(tokenMinus(public_info))
	else:
		itemized_score.append(0)
	if isDiscard(action):	
		itemized_score.append(tokenAdd(public_info))
		itemized_score.append(discardPenalty(public_info))
	else:
		itemized_score += [0] * 2
	# print itemized_score
	return sum(itemized_score)

def _getItemizedScore(atom, public_info, hand, index, k, s, p, d, num_certain_actions):
	if atom[MARK] == set([P]) and not hand[index] in p:
		return boomScore(public_info) / num_certain_actions + discardScore(atom, hand[index], public_info, k, s, d)
	if hand[index] in k and atom[MARK] == set(D):
		return failureScore() / num_certain_actions
	if hand[index] in p and not P in atom[MARK]:
		return wrongMark(atom, public_info)
	if hand[index] in d and not D in atom[MARK]:
		return wrongMark(atom, public_info)
	if atom[MARK] == set([P]):
		return playMarkScore(public_info) + keepScore(hand[index], public_info, k, s)
	if hand[index] in D and atom[MARK] == set([D]):
		return discardMarkScore(public_info)
	if atom[MARK] == set([D]):
		return 0
	score = knowledgeScore(atom, public_info)
	if K in atom[MARK] and not D in atom[MARK]:
		return knowledgeScore(atom, public_info) + keepScore(hand[index], public_info, k, s)
	return knowledgeScore(atom, public_info)
