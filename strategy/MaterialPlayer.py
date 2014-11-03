from person import Person
import random


class MaterialPlayer(Person):
    difficulty = 2

    def __init__(self, name, the_board):
        super(MaterialPlayer, self).__init__(name, the_board)
        self.age = 1
        self.my_player_action = 'discardCard'
        self.my_player_card = 0
        self.play_military = False
        self.play_wonder = False

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

        self.play_wonder = False
        if len(self.board.wonders) > 0:
            if not (self.can_afford_wonder and self.board.wonders[0].wonderTotalCost() == 0):
                self.checkNextWonder()  # this checks if your wonder is available
            if self.can_afford_wonder and self.board.wonders[0].wonderTotalCost() == 0:
                self.play_wonder = True

        self.lookAtMilitary()
        if not self.play_military:
            if not self.play_wonder:
                self.chooseAnAction()
            else:
                self.my_player_action = "playWonder"
                self.burnCard()
        return self.my_player_action, self.my_player_card
        # the player_action can be: playCard, discardCard, or playWonder
        # the player_card is the card you either want to play, discard, or use to build the wonder

    def burnCard(self):
        colors = ["green", "gray"]
        card_id = -1
        for color in colors:
            card_id = self.getIdForColor(color)
            if card_id != -1:
                self.my_player_card = self.findMatchingId(card_id)
                break
        if card_id == -1:
            for card in self.cards_CAN_play:
                if card.give_free:
                    card_id = card.id
            for card in self.cards_CANNOT_play:
                if card.give_free:
                    card_id = card.id
            if card_id != -1:
                self.my_player_card = self.findMatchingId(card_id)
            else:
                self.my_player_card = 0
        
    def getIdForColor(self, color):
        card_id = -1
        for card in self.cards_CAN_play:
            if card.color == color:
                card_id = card.id
        for card in self.cards_CANNOT_play:
            if card.color == color:
                card_id = card.id
        return card_id

    def chooseAnAction(self):
        try:
            self.age = self.cards_CAN_play[0].age
        except IndexError:
            self.age = self.cards_CANNOT_play[0].age

        if self.age == 1:
            self.ageOneStrategy()
        elif self.age == 2:
            self.ageTwoStrategy()
        elif self.age == 3:
            self.ageThreeStrategy()
        else:
            self.my_player_action = "discardCard"
            self.my_player_card = 0

    def ageOneStrategy(self):
        self.my_player_action = "playCard"
        material_cards = []
        give_free_cards = []
        for card in self.cards_CAN_play:
            if card.color == "brown" or card.color == "gray":
                material_cards.append(card)
            elif card.give_free:
                give_free_cards.append(card)

        if len(material_cards) > 0:
            for card in material_cards:
                if "/" in card.ability:
                    self.my_player_card = self.findMatchingId(card.id)
                    break
                elif self.neighborDoesNotHaveMaterial(card.ability):
                    self.my_player_card = self.findMatchingId(card.id)
                    break
                else:
                    self.my_player_card = self.findMatchingId(card.id)
        elif len(give_free_cards) > 0:
            for card in give_free_cards:
                if card.color == "yellow":
                    self.my_player_card = self.findMatchingId(card.id)
                    break
                elif card.color == "green" or card.color == "blue":
                    self.my_player_card = self.findMatchingId(card.id)
        else:
            self.my_player_card = 0

    def ageTwoStrategy(self):
        self.ageOneStrategy()

    def ageThreeStrategy(self):
        self.my_player_action = "playCard"
        guilds = []
        blue_cards = []
        for card in self.cards_CAN_play:
            if card.color == "purple":
                guilds.append(card)
            elif card.color == "blue":
                blue_cards.append(card)
        if len(guilds) > 0:
            card_points_current = 0
            card_cost = guilds[0].totalCost()
            card_id = guilds[0].id
            for card in guilds:
                card_points = 0
                if "/" not in card.ability:
                    for special_ability in card.ability.split(" & "):
                        card_points += self.pointsForEndCard(special_ability)
                else:
                    self.any_science += 1
                    card_points = self.highestScienceValue()
                    self.any_science -= 1
                    card_points -= self.highestScienceValue()
                if card_points > card_points_current or (card_points == card_points_current
                                                         and card.totalCost() < card_cost):
                    card_id = card.id
                    card_points_current = card_points
                    card_cost = card.totalCost()
        elif len(blue_cards) > 0:
            card_points = int(blue_cards[0].ability)
            card_cost = blue_cards[0].totalCost()
            card_id = blue_cards[0].id
            for card in blue_cards:
                if int(card.ability) > card_points or (int(card.ability) == card_points
                                                       and card.totalCost() < card_cost):
                    card_id = card.id
                    card_points = int(card.ability)
                    card_cost = card.totalCost()
        else:
            try:
                card_id = self.cards_CAN_play[0].id
            except IndexError:
                card_id = self.cards_CANNOT_play[0].id
                self.my_player_action = "discardCard"

        self.my_player_card = self.findMatchingId(card_id)

    def lookAtMilitary(self):
        self.play_military = False
        military = []
        if (len(self.cards_CAN_play) + len(self.cards_CANNOT_play)) < 4 and (self <= self.neighbor["left"]
                                                                             or self <= self.neighbor["right"]):
            for card in self.cards_CAN_play:
                if card.color == "red":
                    self.play_military = True
                    military.append(card)

        if self.play_military:
            self.my_player_action = "playCard"
            slim_military = []
            slimmer_military = []
            cheapest_military = military[0]
            cheapest_cost = military[0].totalCost()
            for card in military:
                if card.isFree() or card.give_free:
                    slim_military.append(card)
                    if card.isFree() and card.give_free:
                        slimmer_military.append(card)
                if card.totalCost() < cheapest_cost:
                    cheapest_military = card
                    cheapest_cost = card.totalCost()

            if len(slim_military) == 0:
                self.my_player_card = self.findMatchingId(cheapest_military.id)
            elif len(slim_military) == 1:
                self.my_player_card = self.findMatchingId(slim_military[0].id)
            elif len(slimmer_military) > 0:
                self.my_player_card = self.findMatchingId(slimmer_military[0].id)
            else:
                random.shuffle(slim_military)
                self.my_player_card = self.findMatchingId(slim_military[0].id)

    def findMatchingId(self, card_id):
        for index, card in enumerate(self.cards_CAN_play):
            if card.id == card_id:
                return index
        for index, card in enumerate(self.cards_CANNOT_play):
            if card.id == card_id:
                return len(self.cards_CAN_play) + index

    def neighborDoesNotHaveMaterial(self, ability):
        for key, value in self.neighbor["left"].board.material.items():
            if key == ability and value > 0:
                return False
        for key, value in self.neighbor["right"].board.material.items():
            if key == ability and value > 0:
                return False
        return True
