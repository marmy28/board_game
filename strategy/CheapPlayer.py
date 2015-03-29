from person import Person


class CheapPlayer(Person):
    """This player will look for the cheapest cards to play."""
    difficulty = 2

    def __init__(self, name, the_board):
        super(CheapPlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        player_action, player_card = self.makeDecision()
        return player_action, player_card

    def makeDecision(self):
        if self.can_afford_wonder and len(self.board.wonders) > 0:
            if self.board.wonders[0].wonderTotalCost() == 0:
                return "playWonder", self.burnCard()
        will_play = []
        for card in enumerate(self.cards_CAN_play):  # card[0] is index, card[1] is card
            if card[1].give_free and card[1].isFree() and card[1].age <= 2:  # this will only work for age 1 and 2
                will_play.append(card)
            elif card[1].isFree() and card[1].age == 3:
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
        color = self.getNeighborColor()
        for index, card in enumerate(self.cards_CANNOT_play):
            if card.color == color:
                return index + len(self.cards_CAN_play)
        if len(self.cards_CANNOT_play) != 0:
            return len(self.cards_CAN_play)  # returns the first card in cards_CANNOT_play
        else:
            return 0

    def getNeighborColor(self):
        try:
            age = self.cards_CAN_play[0].age
        except IndexError:
            age = self.cards_CANNOT_play[0].age

        card_direction = {1: 'left', 2: 'right', 3: 'left'}
        max_color = 'green'
        max_length = 0
        for color in self.neighbor[card_direction[age]].cards_played.keys():
            if color != 'wonder':
                if len(self.neighbor[card_direction[age]].cards_played[color]) > max_length:
                    max_length = len(self.neighbor[card_direction[age]].cards_played[color])
                    max_color = color
        return max_color
