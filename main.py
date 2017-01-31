#!/usr/bin/env python
# -*- coding: utf-8 -*-

from judge import Judge
from player import Player
from cheating_player import CheatingPlayer
from const import TEST_DIRECTORY
from os import walk
from card import Card

def getDeck(example_file):
	f = open(example_file)
	raw_deck = f.readlines()
	deck = []
	for card in raw_deck:
		deck.append(Card(int(card[0]), card[1]))
	f.close()
	return deck

all_filenames = []
for (dirpath, dirnames, filenames) in walk(TEST_DIRECTORY):
	for fn in filenames:
		all_filenames.append((dirpath, fn))

all_filenames = [(d, f) for (d, f) in all_filenames if f.endswith('.txt')]

scores = []
for file in all_filenames:
	example_file = file[0] + file[1]
	# if file[1][:3] != "665":
	# 	continue
	judge = Judge()
	judge.takeDeck(getDeck(example_file))
	# judge.takePlayer([Player(judge, "小娘炮"), Player(judge, "云云哥哥")])
	player1 = CheatingPlayer(judge, "小娘炮")
	player2 = CheatingPlayer(judge, "云云哥哥")
	player1.setOther(player2)
	player2.setOther(player1)
	judge.takePlayer([player1, player2])
	judge.byStep = True
	judge.setMute()
	judge.start()
	if judge.getScore() != 25:
		print file[1], judge.getScore()
	scores.append(judge.getScore())
print sum(scores) * 1.0 / len(scores)
print sum([s == 25 for s in scores])

# to_print = {}
# for param in xrange(0, 30):
# 	scores = []
# 	for file in all_filenames:
# 		example_file = file[0] + file[1]
# 		judge = Judge()
# 		judge.takeDeck(getDeck(example_file))
# 		# judge.takePlayer([Player(judge, "小娘炮"), Player(judge, "云云哥哥")])
# 		player1 = CheatingPlayer(judge, "小娘炮")
# 		player2 = CheatingPlayer(judge, "云云哥哥")
# 		player1.param = param
# 		player2.param = param
# 		player1.setOther(player2)
# 		player2.setOther(player1)
# 		judge.takePlayer([player1, player2])
# 		judge.byStep = True
# 		judge.setMute()
# 		# print file[1]
# 		judge.start()
# 		scores.append(judge.getScore())
# 	to_print[param] = sum([s == 25 for s in scores])
# print to_print
