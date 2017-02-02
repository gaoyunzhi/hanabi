from const import COLOR
from const import DECK_DISTRIBUTION
from const import TEST_DIRECTORY
from random import shuffle
import os

SHUFFLE_TIMES = 100
TEST_FILE_NUM = 10000
FILE_NAME_LENGH = 4

def genDeck():
	deck = []
	for c in COLOR:
		for x, times in enumerate(DECK_DISTRIBUTION[c]):
			card = str(x) + c
			deck += [card] * times
	for x in xrange(SHUFFLE_TIMES):
		shuffle(deck)
	return deck

if not os.path.exists(TEST_DIRECTORY):
    os.makedirs(TEST_DIRECTORY)

for file_number in xrange(TEST_FILE_NUM):
	file_name = '0' * (FILE_NAME_LENGH - len(str(file_number))) + str(file_number) + '.txt'
	file = open(TEST_DIRECTORY + file_name, 'w')
	file.write('\n'.join(genDeck()))
	file.close()



