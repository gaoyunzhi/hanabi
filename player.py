from hanabi_player_interface import HanabiPlayerInterface
from const import ACTION_ENUM
from const import ACTION_PLAY
from const import ACTION_HINT
from const import ACTION_DISCARD

class Player(HanabiPlayerInterface) :
	def __init__(self, judge):
		self._judge = judge

	def act(self):
		raise NotImplementedError