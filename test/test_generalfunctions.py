import unittest
from strategy.generalfunctions import *


class GeneralTests(unittest.TestCase):

    def test_compareDicts_NoChange(self):
        actual = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        compareDicts(actual)
        expect = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertListOfDictsIsEqual(actual, expect)

    def test_compareDicts_Change(self):
        actual = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}, {"ore": -1, "wood": -2}]
        compareDicts(actual)
        expect = [{"ore": -1, "wood": -2}, {"clay": -1, "stone": -2}]
        self.assertListOfDictsIsEqual(actual, expect)

    def test_whatMaterialColor_Brown(self):
        self.assertEqual(whatMaterialColor("ore"), "brown")

    def test_whatMaterialColor_Gray(self):
        self.assertEqual(whatMaterialColor("loom"), "gray")

    def test_whatMaterialColor_NA(self):
        self.assertEqual(whatMaterialColor("random"), "NA")

    def test_getScienceScore(self):
        self.assertEqual(getScienceScore({"tablet": 1, "wheel": 2, "compass": 1}), 13)

    def assertListOfDictsIsEqual(self, list1, list2):
        if isinstance(list1, list) and isinstance(list2, list):
            i = 0
            list1_copy = list1.copy()
            list2_copy = list2.copy()
            while i < len(list1_copy):
                j = 0
                while j < len(list2_copy):
                    if list1_copy[i] == list2_copy[j]:
                        list2_copy.pop(j)
                        list1_copy.pop(i)
                        i -= 1
                        break
                    else:
                        j += 1
                i += 1

            if list1_copy or list2_copy:
                raise AssertionError("There is something left over in either of the lists: %r or %r\n"
                                     "items left over are: %r and %r" % (list1, list2, list1_copy,
                                                                         list2_copy))
        else:
            # happens when one of the input is not a list
            raise AssertionError("One of these is not a list: %r or %r" % (list1, list2))

    def test_listOfDictsIsEqual_DiffSize(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual([{'ore': -1}], [{'ore': -1}, {'ore': -1, 'wood': -1}])

    def test_listOfDictsIsEqual_DiffSizeWithDuplicates(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual([{'ore': -1}], [{'ore': -1}, {'ore': -1}])

    def test_listOfDictsIsEqual_DiffSizeWithMultipleDuplicates(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual([{'ore': -1}, {'clay': -1}, {'clay': -1}],
                                          [{'ore': -1}, {'ore': -1}, {'clay': -1}])

    def test_listOfDictsIsEqual_DiffType(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual({'ore': -1}, [{'ore': -1}])

    def test_listOfDictsIsEqual_SameSizeDuplicatesFalse(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual([{'ore': -1}, {'ore': -1}],
                                          [{'ore': -1}, {'ore': -1, 'wood': -1}])

    def test_listOfDictsIsEqual_SameSizeTrue(self):
        self.assertListOfDictsIsEqual([{'ore': -1, 'wood': -1}, {'ore': -1}],
                                      [{'ore': -1}, {'ore': -1, 'wood': -1}])

    def test_listOfDictsIsEqual_SameSizeFalse(self):
        with self.assertRaises(AssertionError):
            self.assertListOfDictsIsEqual([{'clay': -1, 'wood': -1}, {'ore': -1}],
                                          [{'ore': -1}, {'ore': -1, 'wood': -1}])

    def test_buyWithSplit_True(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "wood": -1}]
        self.assertTrue(buyWithSplit(cost_of_card, split), msg="Should return True since you can buy.")

    def test_buyWithSplit_Dict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        expect = [{'ore': -1}, {'wood': -1}, {'clay': -1}, {'stone': -1}]
        actual = buyWithSplit(cost_of_card, split)
        self.assertListOfDictsIsEqual(actual, expect)

    def test_buyWithSplit_StartWithDict(self):
        split = {0: {'ore': 1, 'wood': 1}, 1: {'stone': 1, 'clay': 1}}
        cost_of_card = {"ore": -1, "wood": -1}
        expect = [{'ore': -1}, {'wood': -1}]
        actual = buyWithSplit(cost_of_card, split)
        self.assertListOfDictsIsEqual(actual, expect)

    def test_eraseMoreExpensive_NoChange(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertListOfDictsIsEqual(actual, expect)

    def test_eraseMoreExpensive_Change(self):
        cost_of_card = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}, {"ore": -1, "wood": -2}]
        actual = eraseMoreExpensive(cost_of_card)
        expect = [{"ore": -1, "wood": -1}, {"clay": -1, "stone": -1}]
        self.assertListOfDictsIsEqual(actual, expect)

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
        self.assertListOfDictsIsEqual(actual, expect)

    def test_exterminateTooExpensiveOrGray_NoGrayNoChange(self):
        trading_cost = {"right": [2, 4, 1], "left": [1, 0, 1]}
        card_cost = 0
        material = [{"ore": -1}, {"clay": -1}, {"glass": -1}]
        coin_have = 4
        exterminateTooExpensiveOrGray(trading_cost, card_cost, material, coin_have, check_gray=False)
        expect_material = [{"ore": -1}, {"clay": -1}, {"glass": -1}]
        expect_trading_cost = {"right": [2, 4, 1], "left": [1, 0, 1]}
        self.assertListEqual(trading_cost["right"], expect_trading_cost["right"])
        self.assertListEqual(trading_cost["left"], expect_trading_cost["left"])
        self.assertListOfDictsIsEqual(material, expect_material)

    def test_exterminateTooExpensiveOrGray_NoGrayChange(self):
        trading_cost = {"right": [2, 4, 1], "left": [1, 0, 1]}
        card_cost = 0
        material = [{"ore": -1}, {"clay": -1}, {"glass": -1}]
        coin_have = 3
        exterminateTooExpensiveOrGray(trading_cost, card_cost, material, coin_have, check_gray=False)
        expect_material = [{"ore": -1}, {"glass": -1}]
        expect_trading_cost = {"right": [2, 1], "left": [1, 1]}
        self.assertListEqual(trading_cost["right"], expect_trading_cost["right"])
        self.assertListEqual(trading_cost["left"], expect_trading_cost["left"])
        self.assertListOfDictsIsEqual(material, expect_material)

    def test_exterminateTooExpensiveOrGray_GrayChange(self):
        trading_cost = {"right": [2, 4, 1], "left": [1, 0, 1]}
        card_cost = 0
        material = [{"ore": -1}, {"clay": -1}, {"glass": -1}]
        coin_have = 3
        exterminateTooExpensiveOrGray(trading_cost, card_cost, material, coin_have, check_gray=True)
        expect_material = [{"ore": -1}]
        expect_trading_cost = {"right": [2], "left": [1]}
        self.assertListEqual(trading_cost["right"], expect_trading_cost["right"])
        self.assertListEqual(trading_cost["left"], expect_trading_cost["left"])
        self.assertListOfDictsIsEqual(material, expect_material)

    def test_exterminateTooExpensiveOrGray_GrayNoChange(self):
        trading_cost = {"right": [2, 4], "left": [1, 0]}
        card_cost = 0
        material = [{"ore": -1}, {"clay": -1}]
        coin_have = 4
        exterminateTooExpensiveOrGray(trading_cost, card_cost, material, coin_have, check_gray=True)
        expect_material = [{"ore": -1}, {"clay": -1}]
        expect_trading_cost = {"right": [2, 4], "left": [1, 0]}
        self.assertListEqual(trading_cost["right"], expect_trading_cost["right"])
        self.assertListEqual(trading_cost["left"], expect_trading_cost["left"])
        self.assertListOfDictsIsEqual(material, expect_material)

    def test_buyWithSplitTrade_Change(self):
        split = {0: {'ore': 1, 'wood': 1}}
        cost_of_card = [{"ore": -1}, {"clay": -1}]
        trade_cost = {'brown': 2, 'gray': 1}
        coin_array = {"right": [2, 4], "left": [1, 0]}
        side = "left"
        buyWithSplitTrade(cost_of_card, split, trade_cost, coin_array, side)
        expect_coin_cost = {"right": [4, 2], "left": [0, 3]}
        expect_cost_of_card = [{"clay": -1}, {}]
        self.assertListEqual(coin_array["right"], expect_coin_cost["right"])
        self.assertListEqual(coin_array["left"], expect_coin_cost["left"])
        self.assertListOfDictsIsEqual(cost_of_card, expect_cost_of_card)

    def test_expelExtraMaterial_Change(self):
        coin_cost = {"right": [4, 2], "left": [0, 3]}
        cost_of_card = [{"clay": -1}, {}]
        expelExtraMaterial(coin_cost, cost_of_card)
        expect_coin_cost = {"right": [2], "left": [3]}
        expect_cost_of_card = [{}]
        self.assertListEqual(coin_cost["right"], expect_coin_cost["right"])
        self.assertListEqual(coin_cost["left"], expect_coin_cost["left"])
        self.assertListOfDictsIsEqual(cost_of_card, expect_cost_of_card)

    def test_findCheapestTrade(self):
        coin_cost = {"right": [4, 2], "left": [0, 3]}
        expect = {"right": 4, "left": 0}
        self.assertDictEqual(findCheapestTrade(coin_cost), expect)