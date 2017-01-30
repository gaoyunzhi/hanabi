from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD
from action import Action

class Player(HanabiPlayerInterface) :
	def __init__(self, judge, label):
		self._judge = judge
		self.label = label
		self._otherDiscardLoc = 0

	def act(self):
		if self._judge.moreTokenExist() and \
			other_to_discard = self._getOthersHand()[self._otherDiscardLoc]


	def _getOthersHand(self):
		return self._judge.getHands(self).values()[0]
		# action = Action()
		# action.act = ACTION_PLAY
		# action.loc = 0
		# return action
		