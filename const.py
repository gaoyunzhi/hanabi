import os 
COLOR = ["R", "Y", "G", "B", "W"]
NORMAL_COLOR_DISTRIBUTION = [0, 3, 2, 2, 2, 1]
MULTI_COLOR_DISTRIBUTION = [0, 1, 1, 1, 1, 1]
MULTI_COLOR = "C"
DECK_DISTRIBUTION = {}
for c in COLOR:
	DECK_DISTRIBUTION[c] = NORMAL_COLOR_DISTRIBUTION
# DECK_DISTRIBUTION[MULTI_COLOR] = MULTI_COLOR_DISTRIBUTION

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_DIRECTORY = DIR_PATH + "/test/"

NUM_CARDS_IN_HAND = 5
TOKEN_INIT = 8
BOOM_LIMIT = 2
ROUND_AFTER_DECK_EMPTY = 1

MARK = "mark"
POS = "pos_info"
NEG = "neg_info"

P = "to play"
K = "to keep"
D = "to discard"

PKD = {
	P: "P",
	K: "K",
	D: "D",
}