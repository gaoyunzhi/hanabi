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
NUM_CARDS_IN_DECK = "num_cards_in_deck"

def PublicInfo(object):
	def __init__(self, num_player):
		total_card = 0
		init_desk = {}
		for c in DECK_DISTRIBUTION:
			total_card += sum(DECK_DISTRIBUTION[c])
			init_desk[c] = 0
		total_card -= num_player * NUM_CARDS_IN_HAND
		self.num_player = num_player
		self.round = 0
		self.desk = init_desk
		self.discard_deck = {}
		self.token = TOKEN_INIT
		self.boom = 0
		self.act_after_empty = 0
		self.num_cards_in_deck = total_card

	getStringPublicInfo(public_info):
		result = "#" + str(self.round) + " DESK: "
		for c in self.desk:
			result += c + str(self.desk[c]) + " "
		result += "DISCARD:"
		discard = {}
		for c in DECK_DISTRIBUTION:
			discard[c] = []
		for card in self.discard_deck:
			discard[card[1]] += [str(card[0])] * self.discard_deck[card]
		for c in DECK_DISTRIBUTION:
			discard[c].sort()
			result += c + "".join(discard[c]) + " "
		result += " TOKEN:" + str(public_info.token)
		if public_info.boom:
			result += " BOOM:" + str(public_info.boom)
		return result

	def copy(self):
		public_info = PublicInfo(self.num_player)
		public_info.round = self.round
		public_info.desk = self.desk.copy()
		public_info.discard_deck = self.discard_deck.copy()
		public_info.token = self.token
		public_info.boom = self.boom
		public_info.act_after_empty = self.act_after_empty
		public_info.num_cards_in_deck = self.num_cards_in_deck
	

def updatePublicInfo(public_info, action, hand):
	self.round += 1
	if isHint(action):
		public_info.token -= 1
		return
	if public_info.num_cards_in_deck:
		public_info.num_cards_in_deck -= 1
	else:
		public_info.act_after_empty += 1

	card = hand[action[LOC]]
	hand.pop(action[LOC])
	if isPlay(action):
		public_info = _playCard(public_info, card)
	else:
		public_info.token += 1
		public_info = _discardCard(public_info, card)
	
def canPlay(public_info, card):
	return int(self.desk[card[1]]) + 1 == int(card[0])

def _playCard(public_info, card):
	if canPlay(public_info, card):
		self.desk[card[1]] += 1
		if int(card[0]) == len(DECK_DISTRIBUTION[card[1]]) - 1 and \
			public_info.token < TOKEN_INIT:
			public_info.token += 1
	else:
		public_info.boom += 1
		public_info = _discardCard(public_info, card)
	return public_info

def _discardCard(public_info, card):
	self.discard_deck[card] = \
		self.discard_deck.get(card, 0) + 1
	return public_info

def _isPublicInfoValid(public_info):
	return public_info.token <= TOKEN_INIT and \
		public_info.token >= 0 and \
		public_info.boom <= BOOM_LIMIT

def isGameEnds(public_info):
	if not _isPublicInfoValid(public_info):
		return True
	return public_info.act_after_empty == ROUND_AFTER_DECK_EMPTY * public_info.num_player

def getScore(public_info):
	if not _isPublicInfoValid(public_info):
		return 0
	return sum(self.desk.values())

def noToken(public_info):
	return public_info.token == 0

def tokenFull(public_info):
	return public_info.token == TOKEN_INIT

def getPlayableCards(public_info):
	cards = set()
	for c in self.desk:
		num = self.desk[c] + 1
		if num == len(DECK_DISTRIBUTION[c]):
			continue
		cards.add(str(num) + c)
	return cards

def getDiscardableCards(public_info):
	cards = set()
	for c in self.desk:
		for num in xrange(1, self.desk[c] + 1):
			cards.add(str(num) + c)
	return cards

def getUndiscardbleCards(public_info):
	cards = set()
	for c in self.desk:
		for num in xrange(self.desk[c] + 1, len(DECK_DISTRIBUTION[c])):
			card = str(num) + c
			if self.discard_deck.get(card, 0) + 1 == DECK_DISTRIBUTION[c][num]:
				cards.add(card)
	return cards

def getSuggestDiscardCards(public_info):
	cards = set()
	for c in self.desk:
		for num in xrange(self.desk[c] + 4, len(DECK_DISTRIBUTION[c])):
			card = str(num) + c
			if self.discard_deck.get(card, 0) + 1 != DECK_DISTRIBUTION[c][num]:
				cards.add(card)
	return cards

def getPossibleHandCards(public_info):
	cards = set()
	for c in self.desk:
		for num in xrange(1, len(DECK_DISTRIBUTION[c])):
			card = str(num) + c
			current_number = self.discard_deck.get(card, 0)
			if num <=  self.desk[c]:
				current_number += 1
			if current_number < DECK_DISTRIBUTION[c][num]:
				cards.add(card)
	return cards

