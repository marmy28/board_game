import generalfunctions as GF
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
        return self.shield_count >= other.shield_count

    def changeOfStrategy(self):
        # look in change_class.py if need help. will need to change over all of init parameters
        # may make this a definition in generalfunctions.py
        pass  # TODO change of strategy!

    def highestScienceValue(self):
        if self.any_science == 0:
            return GF.getScienceScore(self.science)
        elif self.any_science == 1:
            a = self.science.copy()
            a[min(a, key=a.get)] += 1
            b = self.science.copy()
            b[max(b, key=b.get)] += 1
            return max(GF.getScienceScore(a), GF.getScienceScore(b))
        elif self.any_science == 2:
            a = self.science.copy()
            a[min(a, key=a.get)] += 2
            b = self.science.copy()
            b[max(b, key=b.get)] += 2
            c = self.science.copy()
            c[min(c, key=c.get)] += 1
            c[min(c, key=c.get)] += 1
            return max(GF.getScienceScore(a), GF.getScienceScore(b), GF.getScienceScore(c))

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
                    my_color = GF.whatMaterialColor(ability.split("/")[0])
                    i = len(self.any_material)
                    if my_color == 'brown':
                        self.any_material[i] = {'ore': 1, 'wood': 1, 'clay': 1, 'stone': 1}
                    elif my_color == 'gray':
                        self.any_material[i] = {'glass': 1, 'loom': 1, 'papyrus': 1}
                else:
                    amount_per, coin, color, direction = ability.split()
                    if color in self.neighbor[direction].cards_played:
                        total_amount = int(amount_per)*len(self.neighbor[direction]
                                                           .cards_played[color])
                    else:
                        total_amount = 0
                    self.board.newMaterial(coin, total_amount)
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
                if self.canBuyCard(i):
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
                final_cost[side] = GF.canBuyThroughTrade(needed_materials, self.trade[side]
                                                         , self.neighbor[side].board.material)

            GF.exterminateTooExpensiveOrGray(final_cost, wonder_eval.cost['coin'], needed_materials
                                             , self.board.material['coin'])
            if len(needed_materials) == 0:
                return False

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                if len(self.neighbor[side].board.split_material):
                    GF.buyWithSplitTrade(needed_materials, self.neighbor[side].board.split_material
                                         , self.trade[side], final_cost, side)

            GF.exterminateTooExpensiveOrGray(final_cost, wonder_eval.cost['coin'], needed_materials
                                             , self.board.material['coin'], check_gray=False)
            GF.expelExtraMaterial(final_cost, needed_materials)

            if len(needed_materials) == 0:
                return False

            wonder_eval.trading_cost = GF.findCheapestTrade(final_cost)
            return True

    def canBuyCard(self, card_number):
        card_eval = self.cards_in_hand[card_number]

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
                final_cost[side] = GF.canBuyThroughTrade(needed_materials, self.trade[side]
                                                         , self.neighbor[side].board.material)

            GF.exterminateTooExpensiveOrGray(final_cost, card_eval.cost['coin'], needed_materials
                                             , self.board.material['coin'])
            if len(needed_materials) == 0:
                return False

            for side in sorted(self.trade.keys(), reverse=look_right_then_left):
                if len(self.neighbor[side].board.split_material):
                    GF.buyWithSplitTrade(needed_materials, self.neighbor[side].board.split_material
                                         , self.trade[side], final_cost, side)

            GF.exterminateTooExpensiveOrGray(final_cost, card_eval.cost['coin'], needed_materials
                                             , self.board.material['coin'], check_gray=False)
            GF.expelExtraMaterial(final_cost, needed_materials)

            if len(needed_materials) == 0:
                return False

            card_eval.trading_cost = GF.findCheapestTrade(final_cost)
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
            next_cost = GF.buyWithSplit(needs_materials, self.board.split_material)
            if next_cost == True:
                return True
        else:
            next_cost = [needs_materials]

        GF.compareDicts(next_cost)
        final_cost = GF.buyWithSplit(next_cost, self.any_material)
        if final_cost != True:
            GF.compareDicts(final_cost)
            final_cost = GF.eraseMoreExpensive(final_cost)
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
            if keys in self.trade:
                print '    ', self.trade[keys]
            else:
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
            if self.play_this_card.color not in self.cards_played:
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
            except IndexError as e:
                print 'discardCard function'
                print e.args
                print e.message
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
                except IndexError as e:
                    print 'playWonder function'
                    print e.args
                    print e.message
                    print self.cards_CANNOT_play
                    print self.cards_CAN_play
                    print card_construction_marker
                    print 'ERROR ERROR ERROR'
                    sys.exit(1)
            if 'wonder' not in self.cards_played:
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
            if color in self.neighbor[direction].cards_played:
                total_amount = int(amount_per)*len(self.neighbor[direction].cards_played[color])
            else:
                total_amount = 0

        return total_amount

    def resolveCardAbilityENDOFGAME(self):
        for ability in self.resolve_ability_at_end:
            if ability == "guild either":
                max_points = 0
                for direction in ['right', 'left']:
                    if 'purple' in self.neighbor[direction].cards_played:
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
