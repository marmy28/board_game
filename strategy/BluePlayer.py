from person import Person


class BluePlayer(Person):
    """This player will look for blue cards to play."""
    difficulty = 2

    def __init__(self, name, the_board):
        super(BluePlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        player_action, player_card = self.makeDecision()
        return player_action, player_card

    def makeDecision(self):
        will_play = []
        for card in enumerate(self.cards_CAN_play):  # card[0] is index, card[1] is card
            if card[1].color == 'blue':
                will_play.append(card)

        if len(will_play) == 0:
            return self.minorStrategy()
        if len(will_play) == 1:
            return "playCard", will_play[0][0]
        else:
            cheapest_card = will_play[0][1].totalCost()
            play_card = 0
            for card in will_play:
                card_cost = card[1].totalCost()
                if card_cost < cheapest_card:
                    cheapest_card = card_cost
                    play_card = card[0]
                elif card[1].name == 'palace':
                    play_card = card[0]
                    break
            return "playCard", play_card

    def minorStrategy(self):
        """Will have minor here."""
        if self.can_afford_wonder:
            return "playWonder", self.burnCard()
        elif len(self.cards_CAN_play) == 0 or self.board.material['coin'] < 2:
            return "discardCard", self.burnCard()
        else:
            cheapest_card = self.cards_CAN_play[0].totalCost()
            play_card = 0
            for card in enumerate(self.cards_CAN_play):
                card_cost = card[1].totalCost()
                if card_cost < cheapest_card:
                    cheapest_card = card_cost
                    play_card = card[0]
            return "playCard", play_card

    def burnCard(self):
        for index, card in enumerate(self.cards_CANNOT_play):
            if card.color == 'green':
                return index + len(self.cards_CAN_play)
        if len(self.cards_CANNOT_play) != 0:
            return len(self.cards_CAN_play)  # returns the first card in cards_CANNOT_play
        else:
            return 0
