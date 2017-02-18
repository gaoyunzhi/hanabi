from const import TOKEN_INIT, BOOM_LIMIT, ROUND_AFTER_DECK_EMPTY, DECK_DISTRIBUTION, NUM_CARDS_IN_HAND

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

	def getString(self):
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
		result += " TOKEN:" + str(self.token)
		if public_info.boom:
			result += " BOOM:" + str(self.boom)
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
		return public_info
	
	def update(self, action, hand):
		self.round += 1
		if action.isHint():
			self.token -= 1
			return
		if self.num_cards_in_deck:
			self.num_cards_in_deck -= 1
		else:
			self.act_after_empty += 1

		card = hand[action.loc]
		hand.pop(action.loc)
		if action.isPlay():
			self.playCard(card)
		else:
			self.token += 1
			self.discardCard(card)
	
	def canPlay(self, card):
		return int(self.desk[card[1]]) + 1 == int(card[0])

	def playCard(self, card):
		if self.canPlay(card):
			self.desk[card[1]] += 1
			if int(card[0]) == len(DECK_DISTRIBUTION[card[1]]) - 1 and \
				self.token < TOKEN_INIT:
				self.token += 1
		else:
			public_info.boom += 1
			public_info = self.discardCard(card)
		return public_info

	def discardCard(self, card):
		self.discard_deck[card] = self.discard_deck.get(card, 0) + 1
		return public_info

	def isPublicInfoValid(self):
		return self.token <= TOKEN_INIT and self.token >= 0 and \
			public_info.boom <= BOOM_LIMIT

	def isGameEnds(self):
		if not self.isPublicInfoValid():
			return True
		return self.act_after_empty == ROUND_AFTER_DECK_EMPTY * public_info.num_player

	def getScore(self):
		if not _isPublicInfoValid(self):
			return 0
		return sum(self.desk.values())

	def noToken(self):
		return self.token == 0

	def tokenFull(self):
		return self.token == TOKEN_INIT

	def getPlayableCards(self):
		cards = set()
		for c in self.desk:
			num = self.desk[c] + 1
			if num == len(DECK_DISTRIBUTION[c]):
				continue
			cards.add(str(num) + c)
		return cards

	def getDiscardableCards(self):
		cards = set()
		for c in self.desk:
			for num in xrange(1, self.desk[c] + 1):
				cards.add(str(num) + c)
			flag = False
			for num in xrange(self.desk[c] + 1, len(DECK_DISTRIBUTION[c])):
				if self.discard_deck.get(card, 0) == DECK_DISTRIBUTION[c][num]:
					flag = True
				if flag:
					cards.add(str(num) + c)
		return cards

	def getUndiscardbleCards(self):
		cards = set()
		for c in self.desk:
			for num in xrange(self.desk[c] + 1, len(DECK_DISTRIBUTION[c])):
				card = str(num) + c
				if self.discard_deck.get(card, 0) + 1 == DECK_DISTRIBUTION[c][num]:
					cards.add(card)
				if self.discard_deck.get(card, 0) == DECK_DISTRIBUTION[c][num]:
					break
		return cards

	def getSuggestDiscardCards(self):
		cards = set()
		for c in self.desk:
			for num in xrange(self.desk[c] + 3, len(DECK_DISTRIBUTION[c])):
				card = str(num) + c
				if self.discard_deck.get(card, 0) + 1 != DECK_DISTRIBUTION[c][num]:
					cards.add(card)
		return cards

	def getPossibleHandCards(self):
		cards = set()
		for c in self.desk:
			for num in xrange(1, len(DECK_DISTRIBUTION[c])):
				card = str(num) + c
				current_number = self.discard_deck.get(card, 0)
				if num <=  self.desk[c]:
					current_number += 1
				if current_number < DECK_DISTRIBUTION[c][num]:
					cards[card] = DECK_DISTRIBUTION[c][num] - current_number
		return cards

	def getSuggestedSets(self):
		return [self.getPlayableCards(), self.getDiscardableCards(), 
			self.getUndiscardbleCards(), self.getSuggestDiscardCards(),
			self.getPossibleHandCards()]