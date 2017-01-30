from const import NUM_CARDS_IN_HAND
from const import TOKEN_INIT
from const import ACTION_PLAY
from const import ACTION_DISCARD
from const import ACTION_HINT
from const import COLOR
from const import BOOM_LIMIT
from const import ROUND_AFTER_DECK_EMPTY
import sys, tty, termios, os

class Judge(object):
    def __init__(self):
        self.byStep = False
        self.mute = False

    def takeDeck(self, deck):
        self._deck = deck
        self.desk = {}
        self.actsAfterEmpty = 0
        self.discardedDeck = {}
        self.boom = 0
        self.token = TOKEN_INIT
        self.lastAct = None
        for c in COLOR:
            self.desk[c] = 0

    def takePlayer(self, players):
        self._players = players
        self._hands = {}
        for player in self._players:
            self._hands[player] = []

    def start(self):
        for _ in xrange(NUM_CARDS_IN_HAND):
            for player in self._players:
                self._sendCard(player)
        while not self._isGameEnds():
            for player in self._players:
                self._printGameStatus()
                if self.byStep: 
                    c = self._getch()
                    if c == "c":
                        exit(0)
                action = player.act()  
                if action.act in [ACTION_PLAY, ACTION_DISCARD]:
                    self._actRelatedToCard(player, action.act, action.loc)
                elif action.act == ACTION_HINT:
                    self.populateLocs(action, player)
                    self.token -= 1
                else:
                    raise Error("act not valid")
                self.lastAct = action
                if not self.mute:
                    print player.label, action
                if not self._deck:     
                    self.actsAfterEmpty += 1
                if self._isGameEnds():
                    break
        self._gameEnds()
    
    def populateLocs(self, action, player):
        if action.act != ACTION_HINT:
            raise Error("action must be hint to populate locs")
        for other_player in self._players:
            if other_player != player:
                break
        action.locs = []
        for index, card in enumerate(self._hands[other_player]):
            if action.number != None and card.number == action.number or \
                action.color != None and card.color == action.color:
                action.locs.append(index)

    def _sendCard(self, player):
        if not self._deck:
            return
        self._hands[player].append(self._deck.pop(0))

    def _actRelatedToCard(self, player, act, loc):
        card = self._hands[player][loc]
        self._hands[player].pop(loc)
        self._sendCard(player)  
        if act == ACTION_PLAY:
            self._play(card)
        elif act == ACTION_DISCARD:
            self._discard(card)
        else:
            raise Error("act not valid")

    def _play(self, card):
        if self.desk[card.color] + 1 == card.number:
            self.desk[card.color] += 1
            return
        self.boom += 1
        self._discard(card)

    def _discard(self, card):
        if not str(card) in self.discardedDeck:
            self.discardedDeck[str(card)] = 0
        self.discardedDeck[str(card)] += 1
        self.token += 1

    def _isInvalidState(self):
        if self.token > TOKEN_INIT or self.token < 0:
            return True
        if self.boom > BOOM_LIMIT:
            return True 
        return False

    def _isGameEnds(self):
        if self._isInvalidState():
            return True
        hands = self._hands.values()
        if self.actsAfterEmpty == ROUND_AFTER_DECK_EMPTY  * len(self._players):
            return True
        return False

    def _gameEnds(self):
        self._printGameStatus()
        print "Game Ends with score", self.getScore()

    def _printGameStatus(self):
        if self.mute:
            return
        print "hands:",
        for player in self._players:
            print player.label, [str(card) for card in self._hands[player]], "  ",
        print
        desk = ""
        for c in COLOR:
            desk += c + str(self.desk[c]) + " "
        print "desk: ", desk, 
        print "discarded", 
        for card, number in self.discardedDeck.iteritems():
            print str(card) + ":" + str(number) + ", ",
        print "boom:", self.boom,
        print "token", self.token

    def getScore(self):
        if self._isInvalidState():
            return 0
        return sum(self.desk.values())

    def _getch(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def moreTokenExist(self):
        return self.token > 0

    def isTokenFull(self):
        return self.token == TOKEN_INIT

    def getHands(self, caller):
        hands = self._hands.copy()
        del hands[caller]
        return hands

    def mute(self):
        self.mute = True
        self.byStep = False # no point of mute and by step

