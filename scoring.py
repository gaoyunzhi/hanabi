from const import BOOM_LIMIT, TOKEN_INIT, NUM_CARDS_IN_HAND
from public_info import BOOM, TOKEN, DESK
LAST_TOKEN = 300.0
BOOM_PENALTY = 1000

def boomScore(public_info):
	return - BOOM_PENALTY / (BOOM_LIMIT - public_info[BOOM] + 0.001)

def failureScore():
	return boomScore(BOOM_LIMIT)

def wrongMark(atom, public_info):
	return tokenMinus(public_info) * (2 - atom[POS])

def tokenAdd(public_info):
	return LAST_TOKEN / (public_info[TOKEN] + 1)

def tokenMinus(public_info):
	return - LAST_TOKEN / (public_info[TOKEN] + 0.001)

def keepScore(card, public_info, state, k, s):
 	if card in k:
 		return tokenAdd(public_info) 
 	if card in s:
 		return 0
 	if int(card[1]) == public_info[DESK] + 1:
 		return tokenAdd(public_info) * 0.8
 	if int(card[1]) == public_info[DESK] + 2:
 		return tokenAdd(public_info) / 2

def knowledgeScore(state, atom):
	score = 0.0
	if atom[MARK] == set(D, K) or atom[MARK] == set(D, P):
		score += tokenAdd(public_info) / 5
	score += len(atom[POS]) * tokenAdd(public_info) / 3
	score += len(atom[NEG]) * tokenAdd(public_info) / 3 / 4
	return score

def numActionScore(num, public_info):
	return tokenAdd(public_info) * [0, 0, 1.0, 5.0/3, 9.0/4, 14.0/5][num]

def blockedSpaceScore(space):
	return tokenAdd(public_info) / (NUM_CARDS_IN_HAND - space + 1)

def discardScore(atom, card, public_info, k, s, d):
	if card in k:
		return failureScore()
	if card in s:
		return 0
	if int(card[1]) == public_info[DESK] + 1:
 		return - tokenAdd(public_info) 
 	if int(card[1]) == public_info[DESK] + 1:
 		return - tokenAdd(public_info) * 0.3
 	if card in d:
 		return tokenAdd(public_info) * 0.5
