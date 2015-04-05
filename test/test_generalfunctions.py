import unittest
from strategy.generalfunctions import *


class GeneralTests(unittest.TestCase):

    def test_compareDictsNoChange(self):
        first_dict = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        compareDicts(first_dict)
        second_dict = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertEqual(first_dict, second_dict)

    def test_compareDictsChange(self):
        first_dict = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}, {"ore": -1, "wood": -2}]
        compareDicts(first_dict)
        second_dict = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertEqual(first_dict, second_dict)

    def test_whatMaterialColorBrown(self):
        self.assertEqual(whatMaterialColor("ore"), "brown")

    def test_whatMaterialColorGray(self):
        self.assertEqual(whatMaterialColor("loom"), "gray")

    def test_whatMaterialColorNA(self):
        self.assertEqual(whatMaterialColor("random"), "NA")

    def test_getScienceScore(self):
        self.assertEqual(getScienceScore({"tablet": 1, "wheel": 2, "compass": 1}), 13)

    def test_buyWithSplitTrue(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "wood": -1}]
        self.assertTrue(buyWithSplit(cost_of_card, split), msg="Should return True since you can buy.")

    def test_buyWithSplitDict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        expect = sorted([{'ore': -1}, {'wood': -1}, {'clay': -1}, {'stone': -1}], key=lambda x: x.keys())
        actual = sorted(buyWithSplit(cost_of_card, split), key=lambda x: x.keys())
        self.assertEqual(actual, expect, msg="Should return array with dict.")

    def test_buyWithSplitStartWithDict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = {"ore": -1, "wood": -1}
        expect = sorted([{'ore': -1}, {'wood': -1}], key=lambda x: x.keys())
        actual = sorted(buyWithSplit(cost_of_card, split), key=lambda x: x.keys())
        self.assertEqual(actual, expect, msg="Should return array with dict.")

    def test_eraseMoreExpensiveNoChange(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertEqual(actual, expect)

    def test_eraseMoreExpensiveChange(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}, {"ore": -1, "wood": -2}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertEqual(actual, expect)