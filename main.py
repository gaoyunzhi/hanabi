#!/usr/bin/env python
# -*- coding: utf-8 -*-

from judge import Judge
from player import Player
from const import TEST_DIRECTORY
from os import walk

def getDeck(example_file):
	f = open(example_file)
	raw_deck = f.readlines()
	deck = []
	for card in raw_deck:
		card = card.strip()
		if card:
			deck.append(card)
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
	# if file[1][:3] != "515":
	# 	continue
	judge = Judge(getDeck(example_file))
	player1 = Player(judge, "player1")
	player2 = Player(judge, "player2")
	judge.takePlayer([player1, player2])
	# judge.byStep = True
	# judge.setMute()
	judge.start()
	score2 = judge.getScore()	
	if judge.getScore() != 25:
		print file[1], score1, score2
	scores.append(judge.getScore())
print sum(scores) * 1.0 / len(scores)
print sum([s == 25 for s in scores])