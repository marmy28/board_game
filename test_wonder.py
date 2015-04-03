from unittest import TestCase
from wonder import Wonder


class TestWonder(TestCase):

    def setUp(self):
        self.init_params = {'name': '02-01-14', 'color': 'brown',
                            'coin': 1, 'clay': 0, 'ore': 0, 'stone': 0,
                            'wood': 0, 'glass': 0, 'loom': 0,
                            'papyrus': 0, 'free_from': None, 'ability': 'clay/ore'}
        self.myWonder = Wonder(self.init_params)
        self.trade = {'left': 1, 'right': 0}
        self.myWonder.trading_cost = self.trade

    def test_resetTrade(self):
        self.myWonder.resetTrade()
        self.assertNotEqual(self.myWonder.trading_cost, self.trade, 'Did not reset trade')

    def test_wonderTotalCost(self):
        self.assertEqual(self.myWonder.wonderTotalCost(), 2, 'Total cost is not 2.')