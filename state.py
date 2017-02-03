from const import NUM_CARDS_IN_HAND
from action import LOCS, HINT

MARK = "mark"
STATE = "state"
POS_INFO = "pos_info"
NEG_INFO = "neg_info"
ROUND_GET = "round_get"
DISCARD_LOC = "discard_loc"
HINT_LOC = "hint_loc"

P = "to play"
K = "to keep"
O = "ok to discard"
D = "to discard"

def getInitState():
	return [
		STATE: atom(-1) for _ in xrange(NUM_CARDS_IN_HAND),
		DISCARD_LOC: 0,
		HINT_LOC: 4
	]

def getInitAtom(round):
	atom = {}
	atom[MARK] = set(P, K, O, D)
	atom[POS_INFO] = set()
	atom[NEG_INFO] = set()
	atomp[ROUND_GET] = round
	return atom

def updateFromHint(state, action):
	for index, atom in enumerate(state[STATE]):
		if index in action[LOCS]:
			atom.POS_INFO.add(action[HINT])
		else:
			atom.NEG_INFO.add(action[HINT])
