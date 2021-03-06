import sys, tty, termios, os
from public_info import PublicInfo
from const import NUM_CARDS_IN_HAND

class Judge(object):
    def __init__(self, deck):
        self.byStep = False
        self.mute = False
        self._deck = deck
        self._hands = {}

    def takePlayer(self, players):
        self.publicInfo = publicInfo(len(players))
        self._players = players
        for player in self._players:
            self._hands[player] = []

    def start(self):
        for _ in xrange(NUM_CARDS_IN_HAND):
            for player in self._players:
                self._sendCard(player)
        while not self._isGameEnds(None):
            for player_index, player in enumerate(self._players):
                self._printGameStatus()
                if self.byStep: 
                    c = self._getch()
                    if c == "c":
                        exit(0)
                action = player.act().populateLosd(self._hands[self._getOther(player)])
                if not self.mute:
                    print player.label, action
                for other_player_index, other_player in enumerate(self._players):
                    other_player.postAct(action, 
                        (other_player_index - player_index + len(self._players)) % len(self._players))
                self.publicInfo.update(action, self._hands[player])
                self._sendCard(player)
                if self._isGameEnds(action):
                    break
        self._gameEnds()

    def _sendCard(self, player):
        if (not self._deck) or len(self._hands[player]) == NUM_CARDS_IN_HAND:
            return
        self._hands[player].append(self._deck.pop(0))

    def _getOther(self, player1):
        for player2 in self._players:
            if player2 != player1:
                return player2

    def getOthersHand(self, player):
        return self._hands[self._getOther(player)]

    def getNumMyCard(self, player):
        return len(self._hands[player])

    def getNumOtherCard(self, player):
        return len(self._hands[self._getOther(player)])

    def _isGameEnds(self, action):
        return (action and not action.isValid()) or self.publicInfo.isGameEnds()

    def _gameEnds(self):
        self._printGameStatus()
        if not self.mute:
            print "Game Ends with score", getScore(self.publicInfo)

    def getScore(self):
        return getScore(self.publicInfo)

    def _printGameStatus(self):
        if self.mute:
            return
        print self.publicInfo.getString()
        for player in self._players:
            print player.label, self._getOther(player).getOthersHand()

    def _getch(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def setMute(self):
        self.mute = True
        self.byStep = False # no point of mute and by step