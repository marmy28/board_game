import unittest
from strategy.generalfunctions import *


class GeneralTests(unittest.TestCase):

    def test_compareDicts_NoChange(self):
        actual = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        compareDicts(actual)
        expect = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_compareDicts_Change(self):
        actual = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}, {"ore": -1, "wood": -2}]
        compareDicts(actual)
        expect = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_whatMaterialColor_Brown(self):
        self.assertEqual(whatMaterialColor("ore"), "brown")

    def test_whatMaterialColor_Gray(self):
        self.assertEqual(whatMaterialColor("loom"), "gray")

    def test_whatMaterialColor_NA(self):
        self.assertEqual(whatMaterialColor("random"), "NA")

    def test_getScienceScore(self):
        self.assertEqual(getScienceScore({"tablet": 1, "wheel": 2, "compass": 1}), 13)

    def listOfDictsIsEqual(self, list1, list2):
        if isinstance(list1, list) and isinstance(list2, list):
            compareDicts(list1)
            compareDicts(list2)
            if len(list1) == len(list2):
                count = 0
                for dict_from_list1 in list1:
                    for dict_from_list2 in list2:
                        if dict_from_list1 == dict_from_list2:
                            count += 1
                            break
                if count == len(list1):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def test_listOfDictsIsEqual_DiffSize(self):
        self.assertFalse(self.listOfDictsIsEqual([{'ore': -1}], [{'ore': -1}, {'ore': -1, 'wood': -1}]))

    def test_listOfDictsIsEqual_DiffType(self):
        self.assertFalse(self.listOfDictsIsEqual({'ore': -1}, [{'ore': -1}]))

    def test_listOfDictsIsEqual_SameSizeDuplicatesFalse(self):
        self.assertFalse(self.listOfDictsIsEqual([{'ore': -1}, {'ore': -1}], [{'ore': -1}, {'ore': -1, 'wood': -1}]))

    def test_listOfDictsIsEqual_SameSizeTrue(self):
        self.assertTrue(self.listOfDictsIsEqual([{'ore': -1, 'wood': -1}, {'ore': -1}],
                                                [{'ore': -1}, {'ore': -1, 'wood': -1}]))

    def test_listOfDictsIsEqual_SameSizeFalse(self):
        self.assertFalse(self.listOfDictsIsEqual([{'clay': -1, 'wood': -1}, {'ore': -1}],
                                                 [{'ore': -1}, {'ore': -1, 'wood': -1}]))

    def test_buyWithSplit_True(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "wood": -1}]
        self.assertTrue(buyWithSplit(cost_of_card, split), msg="Should return True since you can buy.")

    def test_buyWithSplit_Dict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        expect = [{'ore': -1}, {'wood': -1}, {'clay': -1}, {'stone': -1}]
        actual = buyWithSplit(cost_of_card, split)
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_buyWithSplit_StartWithDict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = {"ore": -1, "wood": -1}
        expect = [{'ore': -1}, {'wood': -1}]
        actual = buyWithSplit(cost_of_card, split)
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_eraseMoreExpensive_NoChange(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_eraseMoreExpensive_Change(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}, {"ore": -1, "wood": -2}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_canBuyThroughTrade_ReturnedList(self):
        needed_materials = [{"ore": -1, "wood": -1}, {"clay": -2, "stone": -1}, {"glass": -1}]
        trade_cost = {'brown': 2, 'gray': 1}
        neighbors_materials = {"ore": 1, "clay": 2, "glass": 1}
        expect = [2, 4, 1]
        actual = canBuyThroughTrade(needed_materials, trade_cost, neighbors_materials)
        self.assertListEqual(actual, expect)

    def test_canBuyThroughTrade_ModifiedMaterials(self):
        actual = [{"ore": -2, "wood": -1}, {"clay": -1, "stone": -1}, {"glass": -1}]
        trade_cost = {'brown': 2, 'gray': 1}
        neighbors_materials = {"ore": 1, "clay": 1, "glass": 1}
        canBuyThroughTrade(actual, trade_cost, neighbors_materials)
        expect = [{"ore": -1, "wood": -1}, {"stone": -1}, {}]
        self.assertTrue(self.listOfDictsIsEqual(actual, expect))

    def test_exterminateTooExpensiveOrGray_NoGray(self):
        self.fail()