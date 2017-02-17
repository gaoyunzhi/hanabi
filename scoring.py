from const import BOOM_LIMIT, TOKEN_INIT, NUM_CARDS_IN_HAND, MARK, POS, NEG, \
	P, K, D, ROUND_AFTER_DECK_EMPTY, DECK_DISTRIBUTION
from public_info import BOOM, TOKEN, DESK, NUM_PLAYER, NUM_CARDS_IN_DECK

TOKEN_VALUE = 100.0
BOOM_PENALTY = 3000
EPSILON = 0.001

def gameEndBonus(public_info):
	if _getMaxToDiscardAndToPlay(public_info)[1] == 1:
		return 3000
	else:
		return 0

def discardPenalty(public_info):
	if _getMaxToDiscardAndToPlay(public_info)[1] == 1 and public_info[TOKEN] > 0:
		return -3000
	return - TOKEN_VALUE * 2 / (_getMaxToDiscardAndToPlay(public_info)[0] + EPSILON)

def _getMaxToDiscardAndToPlay(public_info):
	play_or_discard = public_info.num_cards_in_deck + public_info[NUM_PLAYER] * ROUND_AFTER_DECK_EMPTY
	to_play = 0
	for c in public_info[DESK]:
		to_play += len(DECK_DISTRIBUTION[c]) - 1 - public_info[DESK][c]
	return max(0, play_or_discard - to_play), to_play

def playMarkScore(public_info):
	return TOKEN_VALUE * 2

def discardMarkScore(public_info):
	to_discard, to_play = _getMaxToDiscardAndToPlay(public_info)
	return TOKEN_VALUE * max(1, (to_discard / (to_play + EPSILON)))

def boomScore(public_info):
	return _boomScore(public_info[BOOM])

def _boomScore(boom_numnber):
	return - BOOM_PENALTY / (BOOM_LIMIT - boom_numnber + EPSILON)

def failureScore():
	return _boomScore(BOOM_LIMIT)

def wrongMark(atom, public_info):
	return tokenMinus(public_info) * (2 - len(atom[POS]))

def tokenAdd(public_info):
	additon = 0
	if public_info[TOKEN] == 0:
		additon = TOKEN_VALUE * 0.3
	return TOKEN_VALUE + public_info[TOKEN] * 1.0 / TOKEN_INIT * TOKEN_VALUE + additon

def tokenMinus(public_info):
	additon = 0
	if public_info[TOKEN] <= 1:
		additon = TOKEN_VALUE * 0.3
	return - (TOKEN_VALUE + (public_info[TOKEN] + 1) * 1.0 / TOKEN_INIT * TOKEN_VALUE) - additon

def keepScore(card, public_info, k, s):
 	if card in k:
 		return TOKEN_VALUE * 2
 	if card in s:
 		return 0
 	return TOKEN_VALUE * [0, 1.0, 0.8, 0.5, 0.1, 1.0][int(card[0])]

def knowledgeScore(atom, public_info):
	score = 0.0
	if atom[MARK] == set([D, K]) or atom[MARK] == set([D, P]):
		score += TOKEN_VALUE / 10
	score += len(atom[POS]) * TOKEN_VALUE / 6
	score += len(atom[NEG]) * TOKEN_VALUE / 6 / 4
	return score

def numActionScore(num, public_info):
	return TOKEN_VALUE * [0, 0, 1.0, 5.0/3, 9.0/4, 14.0/5][num] * 0.3

def blockedSpaceScore(space, public_info):
	return TOKEN_VALUE / (NUM_CARDS_IN_HAND - space + 1)

def discardScore(atom, card, public_info, k, s, d):
	if card in k:
		return failureScore()
	if card in s:
		return 0
 	if card in d:
 		return TOKEN_VALUE * 0.5
 	return - TOKEN_VALUE * [0, 1.0, 0.8, 0.5, 0.1, 1.0][int(card[0])]
