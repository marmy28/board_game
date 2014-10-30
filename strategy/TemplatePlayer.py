from person import Person  # this allows you to use the functions in Person
import random  # I have this because currently random is used.

# The filename and the class must be the same name
# The filename must end with Player.py for it to be recognized


class TemplatePlayer(Person):
    """Change where it says 'CHANGE'"""
    difficulty = 0  # this should be between 1 and 3 signifying how difficult this strategy is
    number_in_options = 0  # how many times it is put in the array which is randomly shuffled
    # number_in_options should be between 1 and 5. 5 making it more likely to be chosen

    def __init__(self, name, the_board):  # leave this alone
        super(TemplatePlayer, self).__init__(name, the_board)  # sends the name and board to Person

    def decisionForTurn(self, check_hand=True):  # this is the function called from the Game class
        """ The following variables may be useful:
         ----------------------------------------------------------------------------------------
         Naming convention:
         MyClass
         useThisForDefinitions
         this_is_a_variable
         ----------------------------------------------------------------------------------------
         self.cards_played['color or wonder'] - array of those color cards or how many wonders you have played
         self.shield_count - shows how many shields you have
         self.use_free_card - if this is True and you are able to play for free then your card will be free
         self.science - dictionary of science options
         self.any_science - how many wildcard sciences you have
         self.any_material - the wildcard brown and grey is held here
         self.blue_points - how many blue points you have
         self.trade - 2d dictionary with direction then color telling how much to each side
         ----------------------------------------------------------------------------------------
         self.board - stored the name, side, wonders, etc
         self.board.material - this is dictionary of all your materials
         self.board.split_material - dictionary of all your split materials
         self.board.wonder - this is where the wonders are held
         self.board.wonder[0].ability - 1 wonders ability
         self.can_afford_wonder - tells if you can afford the next wonder (similar to cards_CAN_play)
         === the wonders are popped out of this array so the 0 will be the next available wonder
         also the wonders have similar variables to the cards shown below
         ----------------------------------------------------------------------------------------
         self.neighbor['right'] - can select anything from above by deleting self and attaching the last part here
         self.neighbor['left'] - same goes for this one too
         self.neighbor['me'] - this just points back at you so you probably will not use this
         ----------------------------------------------------------------------------------------
         self.cards_CAN_play - cards you can afford
         self.cards_CAN_play[0].color - cards color
         self.cards_CAN_play[0].ability - cards ability
         self.cards_CAN_play[0].give_free - whether or not it gives you something later for free
         self.cards_CAN_play[0].totalCost() - returns the total coin cost of card
         self.cards_CAN_play[0].trading_cost - tells how much coin to give to your neighbors
         self.cards_CANNOT_play - cards in your hand that you cannot afford, even through trading
         === when returning the card number 0 through len(self.cards_CAN_play) - 1 will check
         self.cards_CAN_play and len(self.cards_CAN_play) through len(self.cards_CAN_play) +
         len(self.cards_CANNOT_play) - 1
         ----------------------------------------------------------------------------------------
         """
        self.use_free_card = False  # if you are able to play a card for free and this is True then it will be free
        if check_hand:
            self.use_free_card = True
            self.checkCardsInHand()  # keep inside this if statement so it will not be called when playing discard pile
        self.checkNextWonder()  # this checks if your wonder is available

        player_action = self.chooseAnAction()
        player_card = self.chooseACard()
        return player_action, player_card  # the player_action can be: playCard, discardCard, or playWonder
        # the player_card is the card you either want to play,

    def chooseAnAction(self):
        """CHANGE description of how to choose whether to play, discard, or play a wonder"""

        chosen_action = ["playCard", 'discardCard', 'playWonder']
        return chosen_action[0]

    def chooseACard(self):
        """CHANGE description of how to choose the card."""
        try:
            choose_card = random.randint(0, (len(self.cards_CAN_play)+len(self.cards_CANNOT_play)-1))
        except ValueError:
            choose_card = 0
        return choose_card
