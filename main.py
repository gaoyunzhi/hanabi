#!/usr/bin/env python
# -*- coding: utf-8 -*-

from judge import Judge
from player import Player
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

example_file = all_filenames[0][0] + all_filenames[0][1]

judge = Judge()
judge.takeDeck(getDeck(example_file))
judge.takePlayer([Player(judge, "小娘炮"), Player(judge, "云云哥哥")])
judge.start()