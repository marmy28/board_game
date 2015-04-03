import random
from strategy.person import Person


class PlayPlayer(Person):
    """This player tries to play every turn."""
    difficulty = 2

    def __init__(self, name, the_board):
        super(PlayPlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        player_action = self.chooseAnAction(check_hand)
        player_card = self.chooseACard()
        return player_action, player_card

    def chooseAnAction(self, check_hand):
        """Only selects to play a card."""
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        if self.can_afford_wonder:
            chosenAction = "playWonder"
        else:
            chosenAction = "playCard"
        return chosenAction

    def chooseACard(self):
        """Randomly selects card to play."""
        try:
            choose_card = random.randint(0, (len(self.cards_CAN_play)-1))
        except ValueError:
            choose_card = 0
        return choose_card
