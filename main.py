from judge import Judge
from player import Player
from const import TEST_DIRECTORY
from os import walk

def getDeck(example_file):
	f = open(example_file)
	deck = f.readlines()
	deck = [card.strip() for card in deck]
	f.close()
	return deck

all_filenames = []
for (dirpath, dirnames, filenames) in walk(TEST_DIRECTORY):
	for fn in filenames:
		all_filenames.append((dirpath, fn))

all_filenames = [(d, f) for (d, f) in all_filenames if f.endswith('.txt')]

example_file = all_filenames[0][0] + all_filenames[0][1]

judge = Judge()
judge.takeDeck(getDeck(example_file))
player1 = Player(judge)
player2 = Player(judge)
judge.takePlayer(player1, player2)
judge.start()