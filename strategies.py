__author__ = 'matthew'
import generalfunctions as genF
import random
import sys


class Person(object):
    difficulty = 0
    number_in_options = 0

    def __init__(self, name, the_board):
        self.name = name
        self.neighbor = {"right": None, "left": None, "me": self}
        self.board = the_board
        self.cards_in_hand = []
        self.cards_CAN_play = []
        self.cards_CANNOT_play = []
        self.cards_played = {}
        self.trade = {'left': {'brown': 2, 'gray': 2}, 'right': {'brown': 2, 'gray': 2}}
        self.shield_count = 0
        self.military_points_win = 0
        self.military_points_loss = 0
        self.science = {"tablet": 0, "wheel": 0, "compass": 0}
        self.any_science = 0
        self.blue_points = 0
        self.any_material = {}
        self.play_this_card = None
        self.discard_this_card = None
        self.resolve_ability_at_end = []
        self.play_both_cards_at_end = False
        self.played_wonder = False
        self.can_afford_wonder = False
        self.play_discard_pile = False
        self.free_card = [False, False, False]
        self.use_free_card = False

    def __lt__(self, other):
        return self.shield_count < other.shield_count

    def __le__(self, other):
        return self.shield_count <= other.shield_count

    def __gt__(self, other):
        return self.shield_count > other.shield_count

    def __ge__(self, other):
        return  self.shield_count >= other.shield_count

    def changeOfStrategy(self):
        # look in change_class.py if need help. will need to change over all of init parameters
        # may make this a definition in generalfunctions.py
        pass  # TODO change of strategy!

    def highestScienceValue(self):
        if self.any_science == 0:
            return genF.getScienceScore(self.science)
        elif self.any_science == 1:
            a = self.science.copy()
            a[min(a, key=a.get)] += 1
            b = self.science.copy()
            b[max(b, key=b.get)] += 1
            return max(genF.getScienceScore(a), genF.getScienceScore(b))
        elif self.any_science == 2:
            a = self.science.copy()
            a[min(a, key=a.get)] += 2
            b = self.science.copy()
            b[max(b, key=b.get)] += 2
            c = self.science.copy()
            c[min(c, key=c.get)] += 1
            c[min(c, key=c.get)] += 1
            return max(genF.getScienceScore(a), genF.getScienceScore(b), genF.getScienceScore(c))

    def addToScience(self, ability):
        self.science[ability] += 1

    def addToMaterials(self, ability):
        if "/" in ability:
            self.board.newSplitMaterial(ability)
        elif len(ability.split()) == 2:
            self.board.newMaterial(ability.split()[1], int(ability.split()[0]))
        elif len(ability.split()) == 1:
            self.board.newMaterial(ability)

    def addToMilitary(self, ability):
        self.shield_count += int(ability.split()[0])

    def addToBlue(self, ability):
        self.blue_points += int(ability)

    def addToTrading(self, all_ability, age):
        for ability in all_ability.split(" & "):
            if age == 1:
                if ability.split()[1] == "coin":
                    self.board.newMaterial(ability.split()[1], int(ability.split()[0]))
                else:
                    self.trade[ability.split()[1]][ability.split()[0]] = 1
            elif age == 2:
                if "/" in ability:
                    my_color = genF.whatMaterialColor(ability.split("/")[0])
                    i = len(self.any_material)
                    if my_color == 'brown':
                        self.any_material[i] = {'ore': 1, 'wood': 1, 'clay': 1, 'stone': 1}
                    elif my_color == 'gray':
                        self.any_material[i] = {'glass': 1, 'loom': 1, 'papyrus': 1}
                else:
                    amount_per, coin, color, direction = ability.split()
                    try:
                        total_amount = int(amount_per)*len(self.neighbor[direction]
                                                           .cards_played[color])
                    except KeyError:
                        total_amount = 0
                    self.board.newMaterial(coin,total_amount)
            elif age == 3:
                if "coin" in ability:
                    self.addToTrading(ability, 2)
                else:
                    self.resolve_ability_at_end.append(ability)
            elif age == 4:  # this is for the wonders
                if "/" in ability:
                    self.addToTrading(ability, 2)
                else:
                    self.addToTrading(ability, 1)
            else:
                pass

    def addToGuilds(self, all_ability):
        for ability in all_ability.split(" & "):
            if "/" in ability:
                self.any_science += 1
            else:
                self.resolve_ability_at_end.append(ability)

    def addToSpecial(self, ability):
        if ability == "play both cards at end":
            self.play_both_cards_at_end = True
        elif ability == "guild either":
            self.resolve_ability_at_end.append(ability)
        elif ability == "play discard for free":
            self.play_discard_pile = True
        elif ability == "1 card free per age":
            self.free_card = [True, True, True]
        else:
            pass

    def checkCardsInHand(self):
        i = 0
        self.cards_CAN_play = []
        self.cards_CANNOT_play = []
        while i < len(self.cards_in_hand):
            if self.cards_in_hand[i]:
                if self.canBuyCard(i):  # changed from == True...
                    self.cards_CAN_play.append(self.cards_in_hand[i])
                else:
                    self.cards_CANNOT_play.append(self.cards_in_hand[i])
            else:
                pass
            i += 1
        self.cards_in_hand = []

    def checkNextWonder(self):
        self.can_afford_wonder = self.canBuyWonder()

    def canBuyWonder(self):
        if len(self.board.wonders) == 0:
            return False
        wonder_eval = self.board.wonders[0]
        wonder_eval.resetTrade()

        needed_materials = self.checkIfCanBuy(wonder_eval.cost)

        if needed_materials == True:  # leave as == True because may return a dictionary
            return True
        elif needed_materials == False:  # leave as == False because may return a dictionary
            return False
        else:
            final_cost = {}
            if self.neighbor['right'].board.material['coin'] >= self.neighbor['left'].board.material['coin']:
                look_right_then_left = False  # goes left then right
            else:
                look_right_then_left = True  # goes right then left

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                final_cost[side] = genF.canBuyThroughTrade(needed_materials, self.trade[side]
                                                           , self.neighbor[side].board.material)

            genF.exterminateTooExpensiveOrGray(final_cost, wonder_eval.cost['coin'], needed_materials
                                               , self.board.material['coin'])
            if len(needed_materials) == 0:
                return False

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                if len(self.neighbor[side].board.split_material):
                    genF.buyWithSplitTrade(needed_materials, self.neighbor[side].board.split_material
                                           , self.trade[side], final_cost, side)

            genF.exterminateTooExpensiveOrGray(final_cost, wonder_eval.cost['coin'], needed_materials
                                               , self.board.material['coin'], check_gray=False)
            genF.expelExtraMaterial(final_cost, needed_materials)

            if len(needed_materials) == 0:
                return False

            wonder_eval.trading_cost = genF.findCheapestTrade(final_cost)
            return True

    def canBuyCard(self, intCardNumber):
        card_eval = self.cards_in_hand[intCardNumber]

        already_have = self.checkIfNameInCardsInHand(card_eval.name)
        if already_have:
            return False

        if card_eval.free_from != 'FALSE':
            is_free = self.checkIfNameInCardsInHand(card_eval.free_from)
            if is_free:
                return True

        needed_materials = self.checkIfCanBuy(card_eval.cost)

        if needed_materials == True:  # leave as == True because may return a dictionary
            return True
        elif needed_materials == False:  # leave as == False because may return a dictionary
            return False
        else:
            final_cost = {}
            if self.neighbor['right'].board.material['coin'] >= self.neighbor['left'].board.material['coin']:
                look_right_then_left = False  # goes left then right
            else:
                look_right_then_left = True  # goes right then left

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                final_cost[side] = genF.canBuyThroughTrade(needed_materials, self.trade[side]
                                                           , self.neighbor[side].board.material)

            genF.exterminateTooExpensiveOrGray(final_cost, card_eval.cost['coin'], needed_materials
                                               , self.board.material['coin'])
            if len(needed_materials) == 0:
                return False

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                if len(self.neighbor[side].board.split_material):
                    genF.buyWithSplitTrade(needed_materials, self.neighbor[side].board.split_material
                                           , self.trade[side], final_cost, side)

            genF.exterminateTooExpensiveOrGray(final_cost, card_eval.cost['coin'], needed_materials
                                               , self.board.material['coin'], check_gray=False)
            genF.expelExtraMaterial(final_cost, needed_materials)

            if len(needed_materials) == 0:
                return False

            card_eval.trading_cost = genF.findCheapestTrade(final_cost)
            return True

    def checkIfNameInCardsInHand(self, given_name):
        for keys, values in self.cards_played.items():
            i = 0
            while i < len(values):
                if given_name == values[i].name:
                    return True
                i += 1
        if given_name == 'trading post':
            if self.checkIfNameInCardsInHand('west trading post'):
                return True
            elif self.checkIfNameInCardsInHand('east trading post'):
                return True
        return False

    def checkIfCanBuy(self, card_cost):
        need_and_have_materials = {key: self.board.material[key] - card_cost.get(key, 0)
                                   for key in self.board.material.keys()}
        needs_materials = {}
        for keys, values in need_and_have_materials.items():
            if values < 0 and keys != 'coin':
                needs_materials[keys] = values
            elif values < 0 and keys == 'coin':
                return False
        if len(needs_materials) == 0:
            return True
        if len(self.board.split_material) != 0:
            next_cost = genF.buyWithSplit(needs_materials, self.board.split_material)
            if next_cost == True:
                return True
        else:
            next_cost = [needs_materials]

        genF.compareDicts(next_cost)
        final_cost = genF.buyWithSplit(next_cost, self.any_material)
        if final_cost != True:
            genF.compareDicts(final_cost)
            final_cost = genF.eraseMoreExpensive(final_cost)
        return final_cost

    def printMaterials(self):
        print '\nMaterials\n----------'
        for keys, values in self.board.material.items():
            print values, keys
        if len(self.board.split_material) != 0:
            for keys1, value1 in self.board.split_material.items():
                print '1', value1.keys()[0], '/', value1.keys()[1]

    def printName(self):
        print '\nName\n----------'
        for keys, values in self.neighbor.items():
            print ' ', keys, '=', values.name, values.board.name
            try:
                print '    ', self.trade[keys]
            except KeyError:
                print ''

    def printCardsInHand(self):
        if self.can_afford_wonder:
            print 'Can afford wonder'
        else:
            print 'Cannot afford wonder'
        self.printWonders()
        print '\nCards\n----------'
        for i in range(0, len(self.cards_CAN_play)):
            print i, self.cards_CAN_play[i].name, '-->', self.cards_CAN_play[i].ability \
                , '---', self.cards_CAN_play[i].cost, self.cards_CAN_play[i].trading_cost
        print ''
        for i in range(0, len(self.cards_CANNOT_play)):
            print (i+len(self.cards_CAN_play)), self.cards_CANNOT_play[i].name, \
                '-->', self.cards_CANNOT_play[i].ability

    def printPlayedCards(self):
        for color, cards in self.cards_played.items():
            print color
            print '----------'
            for card in cards:
                print card.name, card.ability
            print ''

    def printWonders(self):
        print self.board.name
        print self.board.side
        for wonder in self.board.wonders:
            print wonder.cost
            print wonder.trading_cost
            print wonder.color
            print wonder.ability
            print ''

    def printMisc(self):
        print '\nExtra\n----------'
        print self.shield_count, 'shield(s)'
        print self.military_points_win, 'military win'
        print self.military_points_loss, 'military loss'
        print self.blue_points, 'victory points'
        print self.any_science, 'any science'
        for keys, values in self.science.items():
            print values, keys
        if len(self.any_material) != 0:
            for keys, values in self.any_material.items():
                print '1', values.keys()

    def printCharacter(self):
        self.printName()
        self.printMisc()
        self.printMaterials()
        # self.printCardsInHand()
        self.printPlayedCards()

    def printScore(self):
        self.resolveCardAbilityENDOFGAME()
        total = (self.military_points_win + self.military_points_loss + self.blue_points
                 + self.highestScienceValue() + (self.board.material['coin']/3))
        print 'Military wins', self.military_points_win
        print 'Military losses', self.military_points_loss
        print 'Blue + Other points', self.blue_points
        print 'Science points', self.highestScienceValue()
        print 'Coin points', (self.board.material['coin']/3)
        print '-----'
        print 'Total', total
        return total

    def playCard(self, card_to_play, age):
        try:
            self.play_this_card = self.cards_CAN_play.pop(card_to_play)
            if self.free_card[age-1] and self.use_free_card:
                self.play_this_card.makeFree()
                self.free_card[age-1] = False
        except IndexError:
            if self.free_card[age-1] and self.use_free_card:
                self.play_this_card = self.cards_CANNOT_play.pop(card_to_play - len(self.cards_CAN_play))
                self.play_this_card.makeFree()
                self.free_card[age-1] = False
            else:
                print 'ACTUALLY discard', self.name
                self.discardCard(card_to_play)
        if self.play_this_card is not None:
            try:
                self.cards_played[self.play_this_card.color].append(self.play_this_card)
            except KeyError:
                self.cards_played[self.play_this_card.color] = []
                self.cards_played[self.play_this_card.color].append(self.play_this_card)
            self.discard_this_card = None
            coin_cost = -1 * self.play_this_card.cost['coin']
            self.board.newMaterial(u'coin', coin_cost)
            for direction, amount in self.play_this_card.trading_cost.items():
                coin_cost = -1 * amount
                self.board.newMaterial(u'coin', coin_cost)
                self.neighbor[direction].board.newMaterial(u'coin', abs(coin_cost))

    def discardCard(self, card_to_discard):
        try:
            self.discard_this_card = self.cards_CAN_play.pop(card_to_discard)
        except IndexError:
            try:
                self.discard_this_card = self.cards_CANNOT_play.pop(card_to_discard
                                                                    - len(self.cards_CAN_play))
            except IndexError:
                print self.cards_CANNOT_play
                print self.cards_CAN_play
                print card_to_discard
                print 'ERROR ERROR ERROR'
                sys.exit(1)
        self.discard_this_card.makeFree()
        self.board.newMaterial(u'coin', 3)
        self.play_this_card = None

    def playWonder(self, card_construction_marker):
        if self.can_afford_wonder:
            try:
                self.cards_CAN_play.pop(card_construction_marker)
            except IndexError:
                try:
                    self.cards_CANNOT_play.pop(card_construction_marker
                                               - len(self.cards_CAN_play))
                except IndexError:
                    print self.cards_CANNOT_play
                    print self.cards_CAN_play
                    print card_construction_marker
                    print 'ERROR ERROR ERROR'
                    sys.exit(1)
            if not self.cards_played.has_key('wonder'):
                self.cards_played['wonder'] = []
            self.cards_played['wonder'].append(self.board.wonders[0])
            self.discard_this_card = None
            self.play_this_card = None
            for direction, amount in self.board.wonders[0].trading_cost.items():
                coin_cost = -1 * amount
                self.board.newMaterial(u'coin', coin_cost)
                self.neighbor[direction].board.newMaterial(u'coin', abs(coin_cost))
            self.played_wonder = True
            # putting this here to be able to play this as the last card and then play again
            if self.board.wonders[0].ability[0] == "play both cards at end":
                self.play_both_cards_at_end = True
        else:
            self.discardCard(card_construction_marker)

    def resolveAbility(self):
        if self.played_wonder:
            self.resolveWonderAbility()
            self.played_wonder = False
        elif self.play_this_card is not None:
            self.resolveCardAbility()
        else:
            pass

    def resolveWonderAbility(self):
        i = 0
        while i < len(self.board.wonders[0].color):
            if self.board.wonders[0].color[i] == "blue":
                self.addToBlue(self.board.wonders[0].ability[i])
            elif self.board.wonders[0].color[i] == "yellow":
                self.addToTrading(self.board.wonders[0].ability[i], 4)
            elif self.board.wonders[0].color[i] == "red":
                self.addToMilitary(self.board.wonders[0].ability[i])
            elif self.board.wonders[0].color[i] == "purple":
                self.addToGuilds(self.board.wonders[0].ability[i])
            elif self.board.wonders[0].color[i] == "NA":
                self.addToSpecial(self.board.wonders[0].ability[i])
            i += 1
        self.board.wonders.pop(0)

    def resolveCardAbility(self):
        if self.play_this_card.color == 'brown' or self.play_this_card.color == 'gray':
            self.addToMaterials(self.play_this_card.ability)
        elif self.play_this_card.color == 'blue':
            self.addToBlue(self.play_this_card.ability)
        elif self.play_this_card.color == 'green':
            self.addToScience(self.play_this_card.ability)
        elif self.play_this_card.color == 'red':
            self.addToMilitary(self.play_this_card.ability)
        elif self.play_this_card.color == 'yellow':
            self.addToTrading(self.play_this_card.ability, self.play_this_card.age)
        elif self.play_this_card.color == 'purple':
            self.addToGuilds(self.play_this_card.ability)
        self.play_this_card = None

    def pointsForEndCard(self, ability):
        if "loses" in ability:
            total_amount = abs(self.neighbor[ability.split()[-1]].military_points_loss)
        else:
            amount_per, color, direction = ability.split()
            try:
                total_amount = int(amount_per)*len(self.neighbor[direction].cards_played[color])
            except KeyError:
                total_amount = 0

        return total_amount

    def resolveCardAbilityENDOFGAME(self):
        for ability in self.resolve_ability_at_end:
            if ability == "guild either":
                max_points = 0
                for direction in ['right', 'left']:
                    if self.neighbor[direction].cards_played.has_key('purple'):
                        for purple_card in self.neighbor[direction].cards_played['purple']:
                            card_points = 0
                            for special_ability in purple_card.ability.split(" & "):
                                card_points += self.pointsForEndCard(special_ability)
                            if card_points > max_points:
                                max_points = card_points
                self.blue_points += max_points
            else:
                self.blue_points += self.pointsForEndCard(ability)

    def handCardsToNeighbor(self, direction):
        self.neighbor[direction].cards_in_hand = []
        for card in self.cards_CAN_play:
            card.trading_cost = {'left': 0, 'right': 0}
            self.neighbor[direction].cards_in_hand.append(card)
        for card in self.cards_CANNOT_play:
            card.trading_cost = {'left': 0, 'right': 0}
            self.neighbor[direction].cards_in_hand.append(card)
        self.cards_CAN_play = []
        self.cards_CANNOT_play = []


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


class RandomPlayer(Person):
    """This player chooses randomly. Randomly chooses between playing a card or discarding."""
    difficulty = 1
    number_in_options = 1

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


class BurnPlayer(Person):
    """This player burns every turn and should end up as the richest player at the end of the game."""
    difficulty = 0
    number_in_options = 0

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


class PlayPlayer(Person):
    """This player tries to play every turn."""
    difficulty = 1
    number_in_options = 2

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


class BluePlayer(Person):
    """This player will look for blue cards to play."""
    difficulty = 1
    number_in_options = 2

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


class GreenPlayer(Person):
    """This player will look for green cards to play."""
    difficulty = 1
    number_in_options = 2

    def __init__(self, name, the_board):
        super(GreenPlayer, self).__init__(name, the_board)

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
            if card[1].color == 'green':
                will_play.append(card)

        if len(will_play) == 0:
            return self.minorStrategy()
        if len(will_play) == 1:
            return "playCard", will_play[0][0]
        else:  # look for best green score here...
            cheapest_card = will_play[0][1].totalCost()
            play_card = 0
            for card in will_play:
                card_cost = card[1].totalCost()
                if card_cost < cheapest_card:
                    cheapest_card = card_cost
                    play_card = card[0]
                elif card[1].name == 'school':
                    play_card = card[0]
                    break
            return "playCard", play_card

    def minorStrategy(self):
        """Will have minor here."""

        if len(self.cards_CAN_play) == 0 or self.board.material['coin'] < 2:
            return "discardCard", self.burnCard()
        elif self.can_afford_wonder:
            return "playWonder", self.burnCard()
        else:
            play_card = 0
            for card in enumerate(self.cards_CAN_play):
                if card[1].color == 'gray':
                    play_card = card[0]
                elif card[1].color == 'red' and card[1].totalCost() == 0:
                    play_card = card[0]
            return "playCard", play_card

    def burnCard(self):
        for index, card in enumerate(self.cards_CANNOT_play):
            if card.color == 'red':
                return index + len(self.cards_CAN_play)
        if len(self.cards_CANNOT_play) != 0:
            return len(self.cards_CAN_play)  # returns the first card in cards_CANNOT_play
        else:
            return 0


class RedPlayer(Person):
    """This player will look for red cards to play."""
    difficulty = 1
    number_in_options = 1

    def __init__(self, name, the_board):
        super(RedPlayer, self).__init__(name, the_board)

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
            if card[1].color == 'red':
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
            if card.color == 'gray':
                return index + len(self.cards_CAN_play)
        if len(self.cards_CANNOT_play) != 0:
            return len(self.cards_CAN_play)  # returns the first card in cards_CANNOT_play
        else:
            return 0


class MaterialPlayer(Person):
    """Change where it says 'CHANGE'"""
    difficulty = 0  # this should be between 1 and 3 signifying how difficult this strategy is
    number_in_options = 0  # how many times it is put in the array which is randomly shuffled
    # number_in_options should be between 1 and 5. 5 making it more likely to be chosen

    def __init__(self, name, the_board):  # leave this alone
        super(MaterialPlayer, self).__init__(name, the_board)  # sends the name and board to Person
        self.age = 1
        self.my_player_action = 'discardCard'
        self.my_player_card = 0
        self.play_military = False

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
        if not (self.can_afford_wonder and self.board.wonders[0].wonderTotalCost() == 0) :
            self.checkNextWonder()  # this checks if your wonder is available

        self.lookAtMilitary()
        if not self.play_military:
            self.chooseAnAction()
        return self.my_player_action, self.my_player_card  # the player_action can be: playCard, discardCard, or playWonder
        # the player_card is the card you either want to play,

    def chooseAnAction(self):
        try:
            self.age = self.cards_CAN_play[0].age
        except ValueError:
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
        pass

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
                self.my_player_card = random.shuffle(slim_military)[0]

    def findMatchingId(self, cardId):
        for index, card in enumerate(self.cards_CAN_play):
            if card.id == cardId:
                return index

    def neighborDoesNotHaveMaterial(self, ability):
        for key, value in self.neighbor["left"].board.material.items():
            if key == ability and value > 0:
                return False
        for key, value in self.neighbor["right"].board.material.items():
            if key == ability and value > 0:
                return False
        return True

class CHANGEPlayer(Person):
    """Change where it says 'CHANGE'"""
    difficulty = 0  # this should be between 1 and 3 signifying how difficult this strategy is
    number_in_options = 0  # how many times it is put in the array which is randomly shuffled
    # number_in_options should be between 1 and 5. 5 making it more likely to be chosen

    def __init__(self, name, the_board):  # leave this alone
        super(CHANGEPlayer, self).__init__(name, the_board)  # sends the name and board to Person

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
