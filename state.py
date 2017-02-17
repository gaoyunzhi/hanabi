from const import NUM_CARDS_IN_HAND, DECK_DISTRIBUTION, COLOR, MARK, POS, NEG, P, K, D, PKD
from action import LOCS, LOC, HINT, hint, play, discard, isHint, isDiscard, isPlay
from public_info import ROUND, BOOM, getPlayableCards, getDiscardableCards, \
	getUndiscardbleCards, getSuggestDiscardCards, getPossibleHandCards, NUM_CARDS_IN_DECK, ACT_AFTER_EMPTY
from scoring import boomScore, failureScore, numActionScore, wrongMark, \
	keepScore, blockedSpaceScore, discardScore, tokenMinus, tokenAdd, knowledgeScore, discardPenalty, playMarkScore, \
	discardMarkScore, gameEndBonus

class State(object):
	def __init__(self):
		self.cards = [Card() for x in xrange(NUM_CARDS_IN_HAND)]
		self.discard_rank = xrange(NUM_CARDS_IN_HAND)

	def copy(self):
		state = State()
		state.cards = [c.copy() for c in self.cards]
		state.discard_rank = list(self.discard_rank)
		return state

	def updateFromHint(self, action, public_info):
		for index, card in enumerate(self.cards):
			if index in action[LOCS]:
				self.pos.add(action.hint)
			else:
				self.neg.add(action.hint)
		self.updateFromPublicInfo(public_info)

	def updateFromOwnAction(state, action):
		if action.loc == None:
			return
		self.cards.pop(action.loc)
		new_discard_rank = []
		for rank in self.discard_rank:
			if rank < action.loc:
				new_discard_rank.append(rank)
			if index > action.loc:
				new_discard_rank.append(rank - 1)
		self.discard_rank = new_discard_rank

	def updateFromOtherAction(state, others_state, action, public_info):
		updateFromPublicInfo(state, public_info)
		updateFromPublicInfo(others_state, public_info)
		if not isHint(action):
			possiblities = getCertainActionFromState(others_state)
			if not action.loc in [a[LOC] for a in possiblities]:
				return
			if not P in self.cards[state[HINT_LOC]][MARK] or self.cards[state[HINT_LOC]][MARK] == set([P]):
				return 
			index = [a[LOC] for a in possiblities].index(action.loc)
			for _ in xrange(index):
				if self.cards[state[HINT_LOC]][MARK] == set([K, D]):
					self.cards[state[HINT_LOC]][MARK] = set([K])
				if not self.cards[state[HINT_LOC]][MARK] == set([P]):
					self.cards[state[HINT_LOC]][MARK].discard(P)
				state[HINT_LOC] = _findNextHintLoc(state)
			if index != len(possiblities) - 1:
				if self.cards[state[HINT_LOC]][MARK] == set([K, D]):
					self.cards[state[HINT_LOC]][MARK] = set([D])
				else:
					self.cards[state[HINT_LOC]][MARK] = set([P])
			state[HINT_LOC] = _findNextHintLoc(state)
			return
		_updateFromHint(state, action, public_info)
		if not action.hint in COLOR:
			_updateFromNumberHint(state, action, public_info)
		else:
			_updateFromColorHint(state, action, public_info)
		updateFromPublicInfo(state, public_info)

	def _updateFromColorHint(state, action, public_info):
		num = len(self.cards)
		for offset in xrange(num):
			for loc in action[LOCS]:
				discard_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
				if D in self.cards[discard_loc][MARK]:
					state[DISCARD_LOC] = discard_loc
					return
		state[DISCARD_LOC] = discard_loc

	def _updateFromNumberHint(state, action, public_info):
		num = len(self.cards)
		for offset in xrange(num):
			for loc in action[LOCS]:
				play_loc = (loc + offset + (public_info[ROUND] + 1) % (num - 1) + num) % num
				if P in self.cards[play_loc][MARK]:
					self.cards[play_loc][MARK] = set([P])
					return
		self.cards[play_loc][MARK] = set([P])

	def updateFromPublicInfo(public_info):
		[p, d, k, s, a] = [getPlayableCards(public_info), getDiscardableCards(public_info), 
			getUndiscardbleCards(public_info), getSuggestDiscardCards(public_info),
			getPossibleHandCards(public_info)]
		if public_info.act_after_empty == 0 and len(self.cards) < NUM_CARDS_IN_HAND:
			self.cards.append(Card())
		else:
			return
		hint_debt = sum([c.needKeep(k) for c in self.cards])
		self.discard_rank = self.discard_rank[: - hint_debt + len(self.discard_rank)] + \
			[len(self.cards) - 1] + self.discard_rank[- hint_debt + len(self.discard_rank):]

class Card(object):
	def _init__(self):
		self.pos = set()
		self.neg = set()
		self.likely = set()
		self.unlikely = set()
		self.hint_not_discard = False

	def getPossibleSet(atom, a):
		colors = set(COLOR)
		if self.pos & colors:
			colors = self.pos & colors
		else:
			colors -= self.neg
		numbers = set(xrange(1, len(DECK_DISTRIBUTION[COLOR[0]])))
		if self.pos & numbers:
			numbers = self.pos & numbers
		else:
			numbers -= self.neg
		possibleSet = set()
		for c in colors:
			for num in numbers:
				possibleSet.add(str(num) + c)
		possibleSet &= a
		return possibleSet

	def needKeep(self, k):
		if self.hint_not_discard:
			return True
		if self.toCard(s)

	def copy(self):
		card = Card()
		card.pos = set(self.pos)
		card.neg = set(self.neg)
		card.likely = set(self.likely)
		card.unlikely = set(self.unlikely)
		card.hint_not_discard = self.hint_not_discard
		return card

	def toCard(self, a):
		possibleSet = _getPossibleSet(atom, a)
		if len(possibleSet) == 1:
			return next(iter(possibleSet))
		return None

	def getString(self):
		result = card[:]
		if len(self.pos) == 1:
			if next(iter(self.pos)) in COLOR:
				result = card[0] + '[' + card[1] + ']'
			else:
				result = '[' + card[0] + ']' + card[1]
		elif len(self.pos) == 2:
			result = '[' + card + ']'
		return result