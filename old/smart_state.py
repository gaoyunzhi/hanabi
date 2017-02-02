from const import NUM_CARDS_IN_HAND
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action
from knowledge import Knowledge

class SmartState(object):
	def __init__(self, player):
		self.discardLoc = 0
		self._player = player
		self.toPlay = None
		self.knowledges = [Knowledge(player) for _ in xrange(NUM_CARDS_IN_HAND)]

	def getPlayPotentials(self):
		potentials = set(self._getCertainPlayLocs(self.knowledges))
		if self.toPlay:
			potentials.add(self.toPlay)
		potentials = list(potentials)
		potentials.sort()
		return potentials

	def getPlayAction(self):
		potentials = self.getPlayPotentials()
		if not potentials:
			return
		action = Action()
		action.act = ACTION_PLAY
		action.loc = potentials[0]
		# which one to choice might help other play, todo
		return action

	def getDiscardAction(self):
		if set(self._getCertainDiscardLocs(self.knowledges)):
			loc = list(self._getCertainDiscardLocs(self.knowledges))[0]
		else:
			self.discardLoc = self._getNewDiscardLoc(self.discardLoc, self.knowledges)
			loc = self.discardLoc
		action = Action()
		action.act = ACTION_DISCARD
		action.loc = loc 
		return action

	def _getNewDiscardLoc(self, loc, knowledges):
		for i in xrange(NUM_CARDS_IN_HAND):
			newLoc = (loc + i) % len(knowledges)
			if knowledges[newLoc].containedIn(self._player.getDangerousSet()):
				continue
			return newLoc
		return 0

	def isDangerous(self, hand):
		if self._getCertainDiscardLocs(self.knowledges):
			return False
		if self.getPlayPotentials(self.knowledges):
			return False
		self.discardLoc = self._getNewDiscardLoc(self.discardLoc, self.knowledges)
		if str(hand[self.discardLoc]) in self._player.getDangerousSet():
			return True
		return False

	def isPotentiallyDangerous(self, hand):
		if self.isDangerous(hand):
			return True
		# TODO
		return False

	def updateFromHint(self, action):
		if action.act != ACTION_HINT:
			return
		for loc in action.locs:
			self.knowledges[loc].updateFromHint(action)
		if action.number != None:
			self.toPlay, _ = self.getPlayResultFromHint(action)
		if action.color != None:
			self.discardLoc, _, _ = self.getDiscardResultFromHint(action)

	def _getDiscardLocFromHint(self, locs, knowledges):
		for shift in xrange(NUM_CARDS_IN_HAND):
			if (self.discardLoc + shift) % len(knowledges) in locs:
				newLoc = (self.discardLoc + shift + 1) % len(knowledges)
				break
		return self._getNewDiscardLoc(newLoc, knowledges)

	def getDiscardResultFromHint(self, action):
		if action.act != ACTION_HINT or action.color == None:
			raise Exception("action must be ACTION_HINT on color")
		newKnowledges = [k.copy() for k in self.knowledges]
		for loc in action.locs:
			newKnowledges[loc].updateFromHint(action)
		return self._getDiscardLocFromHint(action.locs, newKnowledges), \
			self._getCertainDiscardLocs(newKnowledges), \
			self._getCertainPlayLocs(newKnowledges)

	def getPlayResultFromHint(self, action):
		if action.act != ACTION_HINT or action.number == None:
			raise Exception("action must be ACTION_HINT on number")
		newKnowledges = [k.copy() for k in self.knowledges]
		for loc in action.locs:
			newKnowledges[loc].updateFromHint(action)
		return self.getLocationFromHint(action.locs, newKnowledges), self._getCertainPlayLocs(newKnowledges)

	def updateOwnAction(self, action, card):
		if action.act in [ACTION_PLAY, ACTION_DISCARD]:
			del self.knowledges[action.loc]
			# add new card?
			if self.discardLoc > action.loc:
				self.discardLoc -= 1
			if self.toPlay == action.loc:
				self.toPlay = None
			if self.toPlay > action.loc:
				self.toPlay -= 1
		if len(self.knowledges) < NUM_CARDS_IN_HAND and self._player.hasMoreCardsInDeck():
			new_k = Knowledge(self._player)
			for card in self._player.getSeenCards():
				new_k.removePossibility(str(card))
			self.knowledges.append(new_k)

	def updateFromPostActionWithCard(self, action, card):
		[k.removePossibility(card) for k in self.knowledges]

	def _getCertainDiscardLocs(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self._player.getDesk()):
				yield loc

	def _getCertainPlayLocs(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self._player.getCanPlaySet()):
				yield loc

	def getLocationFromHint(self, locs, knowledges):
		markedLocs = set([self._getCertainDiscardLocs(knowledges)] + [self._getCertainPlayLocs(knowledges)])
		for number in xrange(1, NUM_CARDS_IN_HAND):
			for loc in locs:
				potentialLoc = (loc + number) % len(knowledges)
				if not potentialLoc in markedLocs:
					return potentialLoc