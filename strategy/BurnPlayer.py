import random
from person import Person


class BurnPlayer(Person):
    """This player burns every turn and should end up as the richest player at the end of the game."""
    difficulty = 1

    def __init__(self, name, the_board):
        super(BurnPlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        player_action = self.chooseAnAction(check_hand)
        player_card = self.chooseACard()
        return player_action, player_card

    def chooseAnAction(self, check_hand):
        """Only selects discarding."""
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        chosenAction = "discardCard"
        return chosenAction

    def chooseACard(self):
        """Randomly selects card to discard."""
        try:
            choose_card = random.randint(0, (len(self.cards_CAN_play)+len(self.cards_CANNOT_play)-1))
        except ValueError:
            choose_card = 0
        return choose_card
