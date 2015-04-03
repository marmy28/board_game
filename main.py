#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'matthew'

##############
# IMPORTS
##############
import sqlite3
import sys
import random
import strategy
import inspect
from card import Card
from board import Board


##############
# CLASSES
##############

class Game(object):
    """Main class that uses the different strategies and dictates the game flow.

    """

    def __init__(self, number_of_players, difficulty_level, just_computer):
        """Initializes players and their boards. Fetches all the information from the database before
        closing it.

        :param number_of_players: Total number of players, including yourself.
        :type number_of_players: int
        :param difficulty_level: Right now only a 1 or 2, where 2 is more difficult.
        :type difficulty_level: int
        :param just_computer: True if debugging but should be False for you.
        :type just_computer: bool
        :rtype: None

        """

        self.player_name = ['Matthew', 'Kristina', 'Scott', 'Kyle', 'Kevin', 'Katie', 'Jon']
        self.player_strategy = []
        a = inspect.getmodule(strategy)
        for name, obj in inspect.getmembers(strategy, inspect.isclass):
            if hasattr(obj, 'difficulty') and obj.difficulty == difficulty_level:
                if hasattr(obj, 'number_in_options'):
                    i = 0
                    while i < obj.number_in_options:
                        self.player_strategy.append(obj)  # imports strategies from file
                        i += 1
                else:
                    self.player_strategy.append(obj)
        self.player = []
        self.boards = []
        self.age_number = 0  # start at zero until handOutCards
        self.all_cards = {1: [], 2: [], 3: [], 'purple': []}
        self.card_direction = {1: 'left', 2: 'right', 3: 'left'}
        self.discarded_pile = []
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row

        with con:
            cur = con.cursor()
            a_or_b = ['a', 'b']
            cur.execute("SELECT * FROM vBoards WHERE side IS ?", (a_or_b[random.randint(0, 1)],))
            boards = cur.fetchall()
            for board in boards:
                self.boards.append(Board(board, cur))
            for keys, values in self.all_cards.items():
                if keys == 'purple':
                    cur.execute("SELECT * FROM vCards WHERE color = 'purple'")
                else:
                    cur.execute("SELECT * FROM vCards WHERE number_of_players<=:numPlayers \
                    AND age=:age  AND color IS NOT 'purple'", {'numPlayers': number_of_players,
                                                               'age': int(keys)})

                cards = cur.fetchall()
                for card in cards:
                    values.append(Card(card))
        con.close()
        self.shuffleCardsBoardsPlayers(number_of_players)
        self.assignBoardsAndNeighbors(just_computer)

    def shuffleCardsBoardsPlayers(self, num_players):
        """Shuffles the cards, boards, and players. Gets the age III cards in order and gets rid of
        the boards and players not being used.

        :param num_players: Number of players, including yourself.
        :type num_players: int
        :rtype: None

        """
        random.shuffle(self.player_name)
        random.shuffle(self.boards)
        random.shuffle(self.all_cards[1])
        random.shuffle(self.all_cards[2])
        random.shuffle(self.all_cards['purple'])
        i = 0
        while i < (num_players + 2):
            self.all_cards[3].append(self.all_cards['purple'][i])
            i += 1
        random.shuffle(self.all_cards[3])
        self.all_cards.pop('purple')
        while len(self.boards) != num_players:
            self.boards.pop()
        while len(self.player_name) != num_players:
            self.player_name.pop()

    def assignBoardsAndNeighbors(self, just_computer):
        """Assigns the neighbors and the randomly chosen strategy for each person.

        :param just_computer: True when debugging, but should be False for an actual game.
        :type just_computer: bool
        :rtype: None

        """
        i = 0
        if just_computer:
            len_name = len(self.player_name)
        else:
            len_name = len(self.player_name) - 1

        while i < len_name:
            random.shuffle(self.player_strategy)
            chosen_strategy = self.player_strategy[0]
            self.player.append(chosen_strategy(self.player_name[i], self.boards[i]))
            i += 1

        if not just_computer:
            self.player.append(strategy.HumanPlayer(self.boards[-1]))  # this is referenced dynamically
            self.player.reverse()  # so the Human goes first and cannot look at what the others did.

        i = 0
        while i < len(self.player):
            self.player[i].neighbor["left"] = self.player[i-1]
            try:
                self.player[i].neighbor['right'] = self.player[i+1]
            except IndexError:
                self.player[i].neighbor['right'] = self.player[0]

            self.player[i].printName()
            print(self.player[i].__class__.__name__)
            i += 1

    def handOutCards(self):
        """Hands out the cards before each age. This function also prints the scores at the end of the game.

        :rtype: None

        """
        self.age_number += 1
        if self.age_number <= 3:
            i = 0
            while i < len(self.player):
                self.player[i].cards_in_hand = self.all_cards[self.age_number][i*7:(i+1)*7]
                i += 1

            # if self.age_number > 1:
            #     i = 0
            #     while i < len(self.player):
            #         change_strategy = self.player[i].changeOfStrategy()
            #         if change_strategy:
            #             self.player[i] = change_strategy
            #         i += 1
        else:
            print('GAME OVER!')
            final_score = []
            for player in self.player:
                player.printName()
                print('')
                print(player.__class__.__name__)
                print('')
                final_score.append((player.printScore(), player.name, player.__class__.__name__))
            print('\n\n')
            final_score = sorted(final_score, key=lambda tup: tup[0], reverse=True)
            for score, name, class_name in final_score:
                print(name, class_name, score)
            sys.exit(0)  # TODO will put connection to end game here

    def goToNextAge(self):
        """Compares the militaries and gives points accordingly. Finally it goes to self.handOutCards()

        :rtype: None

        """
        military_gain = (2*self.age_number - 1)
        if military_gain > 0:
            for player_military in self.player:

                if player_military > player_military.neighbor['right']:  # this looks at shield_count uses __gt__
                    player_military.military_points_win += military_gain
                    player_military.neighbor['right'].military_points_loss -= 1

                elif player_military < player_military.neighbor['right']:  # this looks at shield_count uses __lt__
                    player_military.military_points_loss -= 1
                    player_military.neighbor['right'].military_points_win += military_gain

                else:
                    player_military.military_points_win += 0
                    player_military.neighbor['right'].military_points_win += 0

        self.handOutCards()

    def aGameTurn(self, turn):
        """Loops through each player and has the player either play a card, wonder, or discard
        according to their choice. This is also where the discard pile obtains cards. If a player
        can look at the discard pile or play both cards at the end they do so here.

        :param turn: The turn of the age.
        :type turn: int
        :rtype: None

        """
        player_can_play_both = ""
        for player_decision in self.player:
            player_action, player_card = player_decision.decisionForTurn()

            if player_action == "playCard":
                player_decision.playCard(player_card, self.age_number)
            elif player_action == "discardCard":
                player_decision.discardCard(player_card)
            elif player_action == "playWonder":
                player_decision.playWonder(player_card)

            if player_decision.discard_this_card is not None:
                self.discarded_pile.append(player_decision.discard_this_card)
                player_decision.discard_this_card = None

            if turn == 5:
                if player_decision.play_both_cards_at_end is False:
                    for last_card in player_decision.cards_CAN_play:
                        self.discarded_pile.append(last_card)
                    for last_card in player_decision.cards_CANNOT_play:
                        self.discarded_pile.append(last_card)
                elif player_decision.play_both_cards_at_end is True:
                    player_can_play_both = player_decision.name

        for player_resolve in self.player:
            player_resolve.resolveAbility()
            if turn != 5:
                player_resolve.handCardsToNeighbor(self.card_direction[self.age_number])

        if self.discarded_pile:
            for player_play_discard in self.player:
                if player_play_discard.play_discard_pile:
                    player_play_discard.cards_CAN_play = self.discarded_pile
                    player_action, player_card = player_play_discard.decisionForTurn(check_hand=False)

                    if player_action == "playCard":
                        player_play_discard.playCard(player_card, self.age_number)
                    elif player_action == "discardCard":
                        player_play_discard.discardCard(player_card)
                    elif player_action == "playWonder":
                        player_play_discard.playWonder(player_card)

                    if player_play_discard.discard_this_card is not None:
                        self.discarded_pile.append(player_play_discard.discard_this_card)
                        player_play_discard.discard_this_card = None

                    player_play_discard.resolveAbility()
                    player_play_discard.cards_CAN_play = []
                    player_play_discard.play_discard_pile = False
                    break

        if player_can_play_both != "":
            print("PLAYING BOTH", player_can_play_both)
            for player_decision in self.player:
                if player_decision.name == player_can_play_both:
                    if player_decision.cards_CAN_play:
                        player_decision.cards_in_hand = player_decision.cards_CAN_play
                    else:
                        player_decision.cards_in_hand = player_decision.cards_CANNOT_play

                    player_action, player_card = player_decision.decisionForTurn()

                    if player_action == "playCard":
                        player_decision.playCard(player_card, self.age_number)
                    elif player_action == "discardCard":
                        player_decision.discardCard(player_card)
                    elif player_action == "playWonder":
                        player_decision.playWonder(player_card)

                    if player_decision.discard_this_card is not None:
                        self.discarded_pile.append(player_decision.discard_this_card)
                        player_decision.discard_this_card = None

                    player_decision.resolveAbility()
                    player_can_play_both = ""
                    break


##############
# MAIN PART
##############

## makes sure that the input is a correct option: 3--7 players


if __name__ == '__main__':
    sys.argv.append(7)
    level = 2
    try:
        int(sys.argv[1])
    except ValueError:
        print("The number of players must be an integer.")
        sys.exit(1)
    except IndexError:
        print("Include the number of players after main.py.")
        sys.exit(1)
    if 2 < int(sys.argv[1]) < 8:
        number_of_players = int(sys.argv[1])
    else:
        print("This game is for 3 to 7 players not %s." % sys.argv[1])
        sys.exit(1)

    play_game = Game(number_of_players, level, just_computer=True)  # change this to true when debugging
    for age in range(0, 4):
        play_game.goToNextAge()
        for turn in range(0, 6):
            play_game.aGameTurn(turn)
