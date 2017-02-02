from const import NUM_CARDS_IN_HAND

MARK = "mark"
POS_INFO = "pos_info"
NEG_INFO = "neg_info"

P = "to play"
K = "to keep"
O = "ok to discard"
D = "to discard"

def getInitState():
	state = {}
	state[MARK] = [set(P, K, O, D) for _ in xrange(NUM_CARDS_IN_HAND)]
	state[POS_INFO] = set()
	state[NEG_INFO] = set()
	return state

