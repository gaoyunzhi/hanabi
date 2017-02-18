from const import NUM_CARDS_IN_HAND, DECK_DISTRIBUTION, COLOR, P, D

MAX_D_SCORE = 0.3
class State(object):
	def __init__(self):
		self.cards = [Card() for x in xrange(NUM_CARDS_IN_HAND)]
		self.discard_rank = xrange(NUM_CARDS_IN_HAND)

	def copy(self):
		state = State()
		state.cards = [c.copy() for c in self.cards]
		state.discard_rank = list(self.discard_rank)
		return state

	def updateFromHint(self, action):
		for index, card in enumerate(self.cards):
			if index in action.locs:
				self.pos.add(action.hint)
			else:
				self.neg.add(action.hint)

	def updateFromOwnAction(self, action):
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

	def getSuggestedSets(self, public_info, others_state, oh = []):
		p, d, k, s, a = public_info.getSuggestedSets()
		other_cards = [c.toCard(a.keys()) for c in others_state.cards]
		other_cards = [c for c in other_cards if c]
		my_cards = [c.toCard(a.keys()) for c in self.cards]
		my_cards = [c for c in my_cards if c]
		d |= set(my_cards) & set(other_cards)

		if oh:
			other_cards_new = oh
		else:
			other_cards_new = other_cards
		for c in other_cards_new:
			a[c] -= 1
			if a[c] = 0:
				del a[c]
		return p, d, k, s, a.keys(), set(oh)

	def getCertainAction(self, public_info, others_state):
		ss = self.getSuggestedSets(public_info, others_state)
		return self.getCertainActionSS(ss)

	def getDiscardScore(self, public_info, others_state, hand):
		ans = self.getPlayScore(self, public_info, others_state, hand)
		actions = [(card.getAction(ss), index) for index, card in enumerate(self.cards)]
		if [action, index for action, index in actions if action[0] == P]:
			return self.getPlayScore(self, public_info, others_state, hand)
		_, index = getCertainActionPrivate(self, public_info, others_state, [])[0]
		if _ == P:
			raise Exception("bug")
		p, d, k, s, a, _ = public_info.getSuggestedSets(public_info, others_state)
		if hand[index] in d:
			return MAX_D_SCORE
		if hand[index] in s:
			return 0.25
		if hand[index] in k:
			return -1
		step = int(hand[index][0]) - public_info.desk[hand[index][1]]
		return [0.05, -0.05, None][step]

	def getPlayScore(self, public_info, others_state, hand):
		ss = self.getSuggestedSets(public_info, others_state)
		actions = [(card.getAction(ss), index) for index, card in enumerate(self.cards)]
		actions.sort(reverse = True)
		actions = [(action[1], index) for action, index in actions if action[0] == P]
		
		last_weight == 0 
		weights = []
		res = []
		for w, i in actions:
			 if w > last_weight:
			 	res.append([i])
			 	weights.append(w)
			 else:
			 	res[-1].append(i)

		ans = 0
		desk = public_info.desk.copy()
		for j, indices in enumerate(res):
			success = True
			for i in indices:
				if desk[hand[i][1]] + 1 != int(hand[i][0]):
					success = False
			if success:
				ans += weights[j] * len(indices)
			else:
				ans -= weights[j]
			for i in indices:
				if desk[hand[i][1]] += 1
		return ans

	def getCertainActionSS(self, ss):
		actions = [(card.getAction(ss), index) for index, card in enumerate(self.cards)]
		actions.sort(reverse = True)
		actions[0][0][0] == None:
			return []
		result = [(x[0], y) for (x, y) in actions if x == actions[0][0]]
		result = result[::-1]
		if actions[0][0] !=  (D, 1):
			result += [(x[0], y) for (x, y) in actions if x == (D, MAX_D_SCORE)]
		return result

	def getCertainActionPrivate(self, public_info, others_state, oh):
		ss = self.getSuggestedSets(public_info, others_state, oh)
		actions = getCertainActionSS(self, ss):
		if not actions:
			loc = self.discard_rank[0]
			if self.cards[self.discard_rank[0]].needKeepStrict():
				loc = self.tryFindFurthestFive(public_info, others_state)
			actions.append((D, loc))
		return actions

	def furthestFive(a, public_info):
		score = []
		for card in a:
			if int(card[0]) != len(DECK_DISTRIBUTION[card[1]]):
				return
			score.append(len(DECK_DISTRIBUTION[card[1]]) - public_info.desk[card[1]])
		return min(score)

	def tryFindFurthestFive(public_info, others_state):
		p, d, k, s, a, oh = self.getSuggestedSets(public_info, others_state)
		ans = []
		for index, c in enumerate(self.state.cards):
			res = self.furthestFive(c.possibleSet(a), public_info)
			if res > 0:
				ans.append((res, index))
		if not ans:
			return self.discard_rank[0]
		return max(ans)[1]
		
	def updateFromOtherAction(self, others_state, action, public_info):
		self.updateFromPublicInfo(public_info, others_state)
		others_state.updateFromPublicInfo(public_info, self)
		if action.isDiscard() and public_info.token > 0 or action.isHint() and action.hint in COLOR:
			for c in self.cards:
				c.unlikely += public_info.getPlayableCards()
		if not action.isHint():
			ps = others_state.getCertainAction(public_info, others_state)
			if not ps:
				return
			if not (action.act, action,loc) in ps:
				print "other player", action.act, "using private info"
				return
			index = ps.find((action.act, action.loc))
			if index == 0:
				continue
			self.cards[self.discard_rank[0]].hint_not_discard = True
			r = self.discard_rank.pop(index)
			self.discard_rank = [r] + self.discard_rank
			self.cards[self.discard_rank[0]].hint_not_discard = False
			return
		if not public_info.isTokenFull():
			for c in self.cards:
				c.likely = set()
		updateFromHint(state, action)
		if not action.hint in COLOR:
			self.updateFromNumberHint(action, public_info, others_state)
		else:
			self.updateFromColorHint(action, public_info, others_state)

	def updateFromColorHint(state, action, public_info, others_state):
		p, d, k, s, a, _ = self.getSuggestedSets(public_info, others_state)
		for index, rank in enumerate(self.discard_rank):
			if rank in action.locs:
				break
		n = len(self.discard_rank) 
		if index == n - 1 and not public_info.isTokenFull():
			self.cards[self.discard_rank[0]].hint_not_discard = True
			return # In great danger, we are
		self.cards[self.discard_rank[0]].hint_not_discard = True
		self.discard_rank = self.discard_rank[(index + 1) % n :] + self.discard_rank[: (index + 1) % n]
		self.discard_rank = [x for x in self.discard_rank if !self.cards[x].needKeepStrict(k, a)] + \
			[x for x in self.discard_rank if self.cards[x].needKeepStrict(k, a)]
		if not self.cards[self.discard_rank[0]].needKeepStrict(k, a):
			self.cards[self.discard_rank[0]].hint_not_discard = False

	def updateFromNumberHint(state, action, public_info, others_state):
		p, d, k, s, a, _ = self.getSuggestedSets(public_info, others_state)
		num = len(self.cards)
		for offset in xrange(num):
			for loc in action.locs:
				play_loc = (loc + offset + (public_info.round + 1) % (num - 1) + num) % num
				if self.cards[play_loc].canPlayStrict([p, a]):
					self.cards[play_loc].likely = p
					return
			for loc in action.locs:
				play_loc = (loc + offset + (public_info.round + 1) % (num - 1) + num) % num
				if self.cards[play_loc].canPlayLoose([p, a]):
					self.cards[play_loc].likely = p
					return				

	def updateFromPublicInfo(public_info, others_state):
		p, d, k, s, a, _ = self.getSuggestedSets(public_info, others_state)
		if public_info.act_after_empty == 0 and len(self.cards) < NUM_CARDS_IN_HAND:
			self.cards.append(Card())
		else:
			hint_debt = sum([c.needKeep(k, a) for c in self.cards])
			self.discard_rank = self.discard_rank[: - hint_debt + len(self.discard_rank)] + \
				[len(self.cards) - 1] + self.discard_rank[- hint_debt + len(self.discard_rank):]
		self.discard_rank = [x for x in self.discard_rank if !self.cards[x].needKeepStrict(k, a)] + \
			[x for x in self.discard_rank if self.cards[x].needKeepStrict(k, a)]

class Card(object):
	def _init__(self):
		self.pos = set()
		self.neg = set()
		self.likely = set()
		self.unlikely = set()
		self.hint_not_discard = False

	def getPossibleSet(self, a):
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

	def canPlayStrict(self, p, a):
		possibleSet = self.getPossibleSet(a)
		possibleSet -= self.unlikely
		return len(possibleSet & p) > 0

	def canPlayLoose(self, p, a):
		possibleSet = self.getPossibleSet(a)
		return len(possibleSet & p) > 0

	def needKeep(self, k, a):
		possibleSet = self.getPossibleSet(a)
		possibleSet -= self.unlikely
		if self.hint_not_discard:
			return True
		if possibleSet <= k:
			return True
		if len(self.likely) > 1 and len(self.likely & k) > len(self.likely) * 0.75:
			return True
		if len(self.possibleSet & k) > len(self.possibleSet) * 0.75:
			return True
		return False

	def needKeepStrict(self, k, s):
		possibleSet = self.getPossibleSet(a)
		if possibleSet <= k:
			return True

	def copy(self):
		card = Card()
		card.pos = set(self.pos)
		card.neg = set(self.neg)
		card.likely = set(self.likely)
		card.unlikely = set(self.unlikely)
		card.hint_not_discard = self.hint_not_discard
		return card

	def toCard(self, a):
		possibleSet = self.getPossibleSet(a)
		if len(possibleSet) == 1:
			return next(iter(possibleSet))
		return None

	def getActionScore(self, ss):
		_, score = self.getAction(ss)
		if score:
			return score
		if not self.hint_not_discard:
			return 0.15
		else:
			return -1

	def getStateAdjuestScore(public_info, orig_state, other_state, hand):
		p, d, k, s, a, _ = self.getSuggestedSets(public_info, other_state, hand)
		adjust = 0.0
		for i, old_card in enumerate(orig_state.cards):
			new_card = self.cards[i]
			if hand[i] in d:
				continue
			if len(old_card.pos) = len(new_card.pos):
				continue
			if len(old_card.getPossibleSet(a - d)) == len(new_card.getPossibleSet(a - d)):
				continue
			hint = next(iter(new_card.pos - old_card.pos))
			if hint in COLOR:
				adjust += 0.01
			else:
				adjust += 0.02
		return adjust

	def getAction(self, [p, d, k, s, a, oh]):
		possibleSet = self.getPossibleSet(a)
		if possibleSet <= p:
			return P, 1
		if self.unlikely and possibleSet - self.unlikely <= p:
			return P, 0.9
		if self.likely and self.likely <= p:
			return P, 0.9
		if self.unlikely and len((possibleSet - self.unlikely) & p) > 0.75 * len((possibleSet - self.unlikely)):
			return P, 0.8
		if self.likely and len(self.likely & p) > 0.75 * len(self.likely):
			return P, 0.8
		if possibleSet <= d:
			return D, MAX_D_SCORE # 0.3
		if self.unlikely and possibleSet - self.unlikely <= d:
			return D, 0.25
		if self.likely and self.likely <= d:
			return D, 0.25
		if possibleSet <= s + d:
			return D, 0.2
		if possibleSet <= s + d + oh
		return None, None

	def getString(self, card):
		result = card[:]
		if len(self.pos) == 1:
			if next(iter(self.pos)) in COLOR:
				result = card[0] + '[' + card[1] + ']'
			else:
				result = '[' + card[0] + ']' + card[1]
		elif len(self.pos) == 2:
			result = '[' + card + ']'
		return result