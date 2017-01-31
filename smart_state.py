from const import NUM_CARDS_IN_HAND
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import action
from knowledge import Knowledge

class SmartState(object):
	def __init__(self, player):
		self.discardLoc = 0
		self._player = player
		self.toPlay = None
		self.knowledges = [Knowledge(player) for _ in xrange(NUM)]

	def updateFromAction(self, action):
		if action.act in [ACTION_PLAY, ACTION_HINT]:
			def self.knowledges[action.loc]
			# add new card?
			if self.discardLoc > action.loc:
				self.discardLoc -= 1
			if self.toPlay > action.loc:
				self.toPlay -= 1

	def getPlayPotentials(self):
		potentials = set(self._getCertainPlayableCards(self.knowledges))
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
		if self._getCertainDiscardLocs():
			loc = self._getCertainDiscardLocs()[0]
		else:
			self.discardLoc = self._getNewDiscardLoc(self.discardLoc, self.knowledges)
			loc = self.discardLoc
		action = Action()
		action.act = ACTION_DISCARD
		action.loc = loc 
		return action

	def getNewDiscardLoc(self, loc, knowledges):
		for i in xrange(NUM_CARDS_IN_HAND):
			newLoc = (loc + i) % NUM_CARDS_IN_HAND
			if knowledges[newLoc].containedIn(self._player.getDangerousSet())
				continue
			return newLoc

	def isDangerous(self, hand):
		if self._getCertainDiscardLocs():
			return False
		if self.getPlayPotentials():
			return False
		self.discardLoc = self._getNewDiscardLoc(self.discardLoc, self.knowledges)
		if hand[self.discardLoc] in self._player.getDangerousSet():
			return True
		return False

	def isPotentiallyDangerous(self, hand):
		if self.isDangerous():
			return True
		# TODO
		return False

	def updateFromHint(self, action)
		if action.act != HINT:
			return
		for loc in action.locs:
			self.knowledges[loc].updateFromHint(action)
		if action.number != None:
			self.toPlay, _ = self.getPlayResultFromHint(action)
		if action.color != None:
			self.discardLoc, _, _ = self.getDiscardResultFromHint(action)

	def _getDiscardLocFromHint(self, action, knowledges):
		if action.act != HINT or action.color == None:
			raise Error("action must be hint on color")
		for shift in xrange(NUM_CARDS_IN_HAND):
			if (self.discardLoc + shift) % NUM_CARDS_IN_HAND in action.locs:
				newLoc = (self.discardLoc + shift + 1) % NUM_CARDS_IN_HAND
		return self._getNewDiscardLoc(newLoc, knowledges)

	def getDiscardResultFromHint(self, action):
		if action.act != HINT or action.color == None:
			raise Error("action must be hint on color")
		newKnowledges = [k.copy() for k in self.knowledges]
		for loc in action.locs:
			newKnowledges[loc].updateFromHint(action)
		return self._getDiscardLocFromHint(action.locs, newKnowledges), 
			self._getCertainDiscardLocs(newKnowledges),
			self._getCertainPlayLocs(newKnowledges)

	def getPlayResultFromHint(self, action):
		if action.act != HINT or action.number == None:
			raise Error("action must be hint on number")
		newKnowledges = [k.copy() for k in self.knowledges]
		for loc in action.locs:
			newKnowledges[loc].updateFromHint(action)
		return self.getLocationFromHint(action.locs, newKnowledges), self._getCertainDiscardLocs(newKnowledges)

	def updateFromPostAction(self, card):
		[k.updateFromPostAction(card) for k in self.knowledges]
		# may need to deal with end situation
		if len(self.knowledges) < NUM_CARDS_IN_HAND:
			new_k = Knowledge(self._player)
			for card in self._player.getSeenCards():
				new_k.removePossibility(str(card))

	def getCertainDiscardLocs(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self.player.getDesk())
				yield loc

	def _getCertainPlayableCards(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self.player.getCanPlaySet())
				yield loc

	def getLocationFromHint(self, locs, knowledges):
		if action.act != HINT or action.number == None:
			raise Error("action must be hint on number")
		knowledges = knowledges || self.knowledges
		markedLocs = set([self._getCertainDiscardLocs(knowledges)] + [self._getCertainPlayableCards(knowledges)])
		for number in xrange(1, NUM_CARDS_IN_HAND):
			for loc in locs:
				potentialLoc = (loc + number) % NUM_CARDS_IN_HAND
				if not potentialLoc in markedLocs:
					return potentialLoc