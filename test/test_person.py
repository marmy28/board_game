from unittest import TestCase
from strategy.person import Person
from card import Card

class TestPerson(TestCase):

    def setUp(self):
        self.me = Person("Matt", None)

    def test_highestScienceValue(self):
        self.me.science = {"tablet": 1, "wheel": 0, "compass": 0}
        self.me.any_science = 2
        self.assertEqual(self.me.highestScienceValue(), 10)

    def test_addToScience(self):
        self.me.addToScience("tablet")
        expect = {"tablet": 1, "wheel": 0, "compass": 0}
        self.assertDictEqual(self.me.science, expect)

    def test_addToMaterials(self):
        self.fail()

    def test_addToMilitary(self):
        self.me.addToMilitary("2 shield")
        self.assertEqual(self.me.shield_count, 2)

    def test_addToBlue(self):
        self.me.addToBlue("7")
        self.assertEqual(self.me.blue_points, 7)

    def test_addToTrading(self):
        self.fail()

    def test_addToGuilds_Science(self):
        self.me.addToGuilds("tablet/wheel/compass")
        self.assertEqual(self.me.any_science, 1)

    def test_addToGuilds_ResolveLater(self):
        self.me.addToGuilds("1 brown me & 1 gray me & 1 purple me")
        expect = ["1 brown me", "1 gray me", "1 purple me"]
        self.assertListEqual(self.me.resolve_ability_at_end, expect)

    def test_addToSpecial_PlayBoth(self):
        self.me.addToSpecial("play both cards at end")
        self.assertTrue(self.me.play_both_cards_at_end)

    def test_addToSpecial_GuildEither(self):
        self.me.addToSpecial("guild either")
        expect = ["guild either"]
        self.assertListEqual(self.me.resolve_ability_at_end, expect)

    def test_addToSpecial_PlayDiscard(self):
        self.me.addToSpecial("play discard for free")
        self.assertTrue(self.me.play_discard_pile)

    def test_addToSpecial_FreeCard(self):
        self.me.addToSpecial("1 card free per age")
        expect = [True, True, True]
        self.assertListEqual(self.me.free_card, expect)

    def test_addToSpecial_Error(self):
        with self.assertRaises(Exception):
            self.me.addToSpecial("Hello")

    def test_checkCardsInHand(self):
        self.fail()

    def test_checkNextWonder(self):
        self.fail()

    def test_canBuyWonder(self):
        self.fail()

    def test_canBuyCard(self):
        self.fail()

    def test_checkIfNameInCardsInHand(self):
        self.fail()

    def test_checkIfCanBuy(self):
        self.fail()

    def test_playCard(self):
        self.fail()

    def test_discardCard(self):
        self.fail()

    def test_playWonder(self):
        self.fail()

    def test_resolveAbility(self):
        self.fail()

    def test_resolveWonderAbility(self):
        self.fail()

    def test_resolveCardAbility_Brown(self):
        self.fail()

    def test_resolveCardAbility_Gray(self):
        self.fail()

    def test_resolveCardAbility_Blue(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'blue',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': '6',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        self.me.resolveCardAbility()
        self.assertEqual(self.me.blue_points, 6)

    def test_resolveCardAbility_Green(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'green',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': 'wheel',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        self.me.resolveCardAbility()
        expect = {"tablet": 0, "wheel": 1, "compass": 0}
        self.assertDictEqual(self.me.science, expect)

    def test_resolveCardAbility_Red(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'red',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': '6 shield',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        self.me.resolveCardAbility()
        self.assertEqual(self.me.shield_count, 6)

    def test_resolveCardAbility_Yellow(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'yellow',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': 'brown left',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        self.me.resolveCardAbility()
        expect = {'brown': 1, 'gray': 2}
        self.assertDictEqual(self.me.trade["left"], expect)

    def test_resolveCardAbility_Purple(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'purple',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': 'guild either',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        self.me.resolveCardAbility()
        expect = ["guild either"]
        self.assertListEqual(self.me.resolve_ability_at_end, expect)

    def test_resolveCardAbility_Error(self):
        init_params = {'id': 3, 'name': 'clay pool', 'color': 'color',
                       'age': 1, 'number_of_players': 3, 'coin': 1, 'clay': 0,
                       'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0,
                       'papyrus': 0, 'free_from': None, 'ability': 'guild either',
                       'give_free': 0}
        self.me.play_this_card = Card(init_params)
        with self.assertRaises(Exception):
            self.me.resolveCardAbility()

    def test_pointsForEndCard(self):
        self.fail()

    def test_resolveCardAbilityENDOFGAME(self):
        self.fail()

    def test_handCardsToNeighbor(self):
        self.fail()