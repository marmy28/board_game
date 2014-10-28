from person import Person

class HumanPlayer(Person):
    """This is the actual player."""
    difficulty = 0  # do not increase this number or else it will be selected automatically
    number_in_options = 0

    def __init__(self, the_board):
        name = raw_input("What is your name? ")
        print "Hello ", name
        super(HumanPlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        player_action, player_card = self.makeDecision()
        return player_action, player_card

    def makeDecision(self):
        me = self
        while True:
            ask = raw_input("lc: left character, rc: right character, m: misc, " +
                            "c: cards in hand, me: me, br: be right character, " +
                            "bl: be left character, bm: be me, n: next\n")
            if ask == "lc":
                me.neighbor['left'].printCharacter()
            elif ask == "rc":
                me.neighbor['right'].printCharacter()
            elif ask == "m":
                me.printMisc()
            elif ask == "c" and me == self:
                me.printCardsInHand()
            elif ask == "me":
                me.printCharacter()
            elif ask == "br":
                me = me.neighbor["right"]
            elif ask == "bl":
                me = me.neighbor["left"]
            elif ask == "bm":
                me = self
            elif ask == "n":
                break

        player_action = raw_input("1: playCard 2: discardCard 3: playWonder? ")
        player_card = int(raw_input("Which card (int)? "))
        if player_action == "1":
            player_action = "playCard"
        elif player_action == "2":
            player_action = "discardCard"
        elif player_action == "3":
            player_action = "playWonder"
        return player_action, player_card
