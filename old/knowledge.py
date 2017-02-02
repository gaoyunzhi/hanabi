class Knowledge(object):
	def __init__(self, player):
		if player:
			self.possibleCard = player.getInitPossibleCards()

	def containedIn(self, aSet):
		return len(set(self.possibleCard.keys()) - set(aSet)) == 0

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
		if self.possibleCard[card] == 0:
			del self.possibleCard[card]

	def copy(self):
		k = Knowledge(None)
		k.possibleCard = self.possibleCard.copy()
		return k