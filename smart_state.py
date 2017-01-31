from const import NUM_CARDS_IN_HAND
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import action

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

	def getPlayAction(self):
		potentials = []
		if self.toPlay:
			potentials.append(self.toPlay)
		potentials.append(self._getCertainPlayableCards(self.knowledges))
		potentials.sort()
		if not potentials:
			return
		action = Action()
		action.act = ACTION_PLAY
		action.loc = potentials[0]
		# which one to choice might help other play, todo
		return action

	def get

	def updateFromHint(self, action)
		if action.act != HINT:
			return
		for loc in action.locs:
			self.knowledges[loc].updateFromHint(action)
		self.toPlay = self.getResultFromHint(action)

	def getResultFromHint(self, action):
		if action.act != HINT:
			raise Error("action must be hint")
		newKnowledges = [k.copy() for k in self.knowledges]
		for loc in action.locs:
			newKnowledges[loc].updateFromHint(action)
		return self.getLocationFromHint(action, action.locs)


	def updateFromPostAction(self, card):
		[k.updateFromPostAction(card) for k in self.knowledges]
		# may need to deal with end situation
		if len(self.knowledges) < NUM_CARDS_IN_HAND:
			new_k = Knowledge(self._player)
			for card in self._player.getSeenCards():
				new_k.removePossibility(str(card))

	def _getCertainDiscardLocs(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self.player.getDesk())
				yield loc

	def _getCertainPlayableCards(self, knowledges):
		for loc, knowledge in enumerate(knowledges):
			if knowledge.containedIn(self.player.getCanPlaySet())
				yield loc

	def getLocationFromHint(self, locs, knowledges):
		knowledges = knowledges || self.knowledges
		markedLocs = set([self._getCertainDiscardLocs(knowledges)] + [self._getCertainPlayableCards(knowledges)])
		for number in xrange(1, NUM_CARDS_IN_HAND):
			for loc in locs:
				potentialLoc = (loc + number) % NUM_CARDS_IN_HAND
				if not potentialLoc in markedLocs:
					return potentialLoc



class Knowledge(object):
	def __init__(self, player):
		if player:
			self.possibleCard = player.getInitPossibleCards()

	def containedIn(self, set):
		return len(self.possibleCard.keys() - set(set)) == 0

	def updateFromHint(self, hint):
		keysToDelete = set()
		for card in self.possibleCard:
			if hint.number != None and int(card[0]) != hint.number:
				keysToDelete.add(card)
			if hint.color != None and card[1] != hint.color:	
				keysToDelete.add(card)
		for key in keysToDelete:
			del self.possibleCard[key]

	def removePossibility(self, card):
		if not card in self.possibleCard:
			return
		self.possibleCard[card] -= 1
		if self.possibleCard[card] == 0：
			del self.possibleCard[card]

	def __copy__(self):
		k = Knowledge(None)
		k.possibleCard = self.possibleCard.copy()
		return k






