import random
from person import Person

class RandomPlayer(Person):
    """This player chooses randomly. Randomly chooses between playing a card or discarding."""
    difficulty = 1

    def __init__(self, name, the_board):
        super(RandomPlayer, self).__init__(name, the_board)

    def decisionForTurn(self, check_hand=True):
        player_action = self.chooseAnAction(check_hand)
        player_card = self.chooseACard()
        return player_action, player_card

    def chooseAnAction(self, check_hand):
        """Makes the random choice between playing or discarding."""
        self.use_free_card = False
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()
        self.checkNextWonder()
        chosenAction = ["playCard", "discardCard", "playWonder"]
        random.shuffle(chosenAction)
        return chosenAction[0]

    def chooseACard(self):
        """Randomly chooses the card to play."""
        num_cards = len(self.cards_CAN_play)+len(self.cards_CANNOT_play)
        try:
            choose_card = random.randint(0, (num_cards-1))
        except ValueError:
            choose_card = 0
        return choose_card
