from unittest import TestCase
from card import Card

__author__ = 'matthew'


class TestCard(TestCase):

    def setUp(self):
        self.init_params = {'id': 3, 'name': 'clay pool', 'color': 'brown',
                            'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                            'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                            'papyrus': 0, 'free_from': None, 'ability': 'clay/ore',
                            'give_free': 0}
        self.myCard = Card(self.init_params)

    def test_makeFree(self):
        materials = {'coin': 0, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0, 'papyrus': 0}
        trade = {'left': 0, 'right': 0}
        self.myCard.makeFree()
        self.assertEqual(self.myCard.trading_cost, trade, 'trade is not free')
        self.assertEqual(self.myCard.cost, materials, 'materials were not cleared')

    def test_totalCost(self):
        self.assertEqual(self.myCard.totalCost(), 1, 'Total cost of card is not 1.')

    def test_isFree(self):
        self.assertFalse(self.myCard.isFree(), 'This card says it is free when it is not.')