ROUND = "round"
DESK = "desk"
DISCARD_DECK = "discard_deck"

def getPublicInfo(round, desk, discard_deck):
	return {
		ROUND: round,
		DESK: desk.copy(),
		DISCARD_DECK: discard_deck.copy()
	}
