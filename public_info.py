from const import TOKEN_INIT, BOOM_LIMIT, ROUND_AFTER_DECK_EMPTY
from const import DECK_DISTRIBUTION
from const import NUM_CARDS_IN_HAND
from action import isHint
from action import isPlay
from action import isDiscard
from action import LOC

ROUND = "round"
DESK = "desk"
DISCARD_DECK = "discard_deck"
TOKEN = "token"
BOOM = "boom"
ACT_AFTER_EMPTY = "act_after_empty"
NUM_PLAYER = "num_player"

def copyPublicInfo(public_info):
	return {
		NUM_PLAYER: public_info[NUM_PLAYER],
		ROUND: public_info[ROUND],
		DESK: public_info[DESK].copy(),
		DISCARD_DECK: public_info[DISCARD_DECK].copy(),
		TOKEN: public_info[TOKEN],
		BOOM: public_info[BOOM],
		ACT_AFTER_EMPTY: public_info[ACT_AFTER_EMPTY],
		NUM_CARDS_IN_DECK: public_info[NUM_CARDS_IN_DECK]
	}

def getInitialPublicInfo(num_player):
	total_card = 0
	init_desk = {}
	for c in DECK_DISTRIBUTION:
		total_card += sum(DECK_DISTRIBUTION[c])
		init_desk[c] = 0
	total_card -= num_player * NUM_CARDS_IN_HAND
	return {
		NUM_PLAYER: num_player,
		ROUND: 0,
		DESK: init_desk,
		DISCARD_DECK: {},
		TOKEN: TOKEN_INIT,
		BOOM: 0,
		ACT_AFTER_EMPTY: 0,
		NUM_CARDS_IN_DECK: total_card 
	}

def updatePublicInfo(public_info, action, hand):
	if isHint(action):
		return
	public_info[ROUND] += 1
	if public_info[NUM_CARDS_IN_DECK]:
		public_info[NUM_CARDS_IN_DECK] -= 1
	else:
		public_info[ACT_AFTER_EMPTY] += 1

	card = hand[action[LOC]]
	hand.pop(action[LOC])
	if isPlay(action):
		public_info[TOKEN] -= 1
		public_info = _playCard(public_info, card)
	else:
		public_info[TOKEN] += 1
		public_info = _discardCard(public_info, card)
	
def canPlay(public_info, card):
	return int(public_info[DESK][card[1]]) + 1 == int(card[0])

def _playCard(public_info, card):
	if canPlay(public_info, card):
		public_info[DESK][card[1]] += 1
		if int(card[0]) == len(DECK_DISTRIBUTION[card[1]]) - 1 and \
			public_info[TOKEN] < TOKEN_INIT:
			public_info[TOKEN] += 1
	else:
		public_info[BOOM] += 1
		public_info = _discardCard(public_info, card)
	return public_info

def _discardCard(public_info, card):
	public_info[DISCARD_DECK][card] = \
		public_info[DISCARD_DECK].get(card, 0) + 1
	return public_info

def _isPublicInfoValid(public_info):
	return public_info[TOKEN] <= TOKEN_INIT and \
		public_info[TOKEN] >= 0 and \
		public_info[BOOM] <= BOOM_LIMIT

def isGameEnds(public_info):
	if not _isPublicInfoValid(public_info):
		return False
	return public_info[ACT_AFTER_EMPTY] == ROUND_AFTER_DECK_EMPTY * public_info[NUM_PLAYER]

def getScore(public_info):
	if not _isPublicInfoValid(public_info):
		return 0
	return sum(public_info[DESK].values())

def noToken(public_info):
	return public_info[TOKEN] == 0

def tokenFull(public_info):
	return public_info[TOKEN] == TOKEN_INIT