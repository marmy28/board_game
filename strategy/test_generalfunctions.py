import unittest
from strategy.generalfunctions import *


class GeneralTests(unittest.TestCase):

    def test_compareDictsNoChange(self):
        first_dict = [{"ore": 1, "wood": 2}, {"clay": 1, "stone": 2}]
        compareDicts(first_dict)
        second_dict = [{"ore": 1, "wood": 2}, {"clay": 1, "stone": 2}]
        self.assertEqual(first_dict, second_dict)

    def test_compareDictsChange(self):
        first_dict = [{"ore": 1, "wood": 2}, {"clay": 1, "stone": 2}, {"ore": 1, "wood": 2}]
        compareDicts(first_dict)
        second_dict = [{"ore": 1, "wood": 2}, {"clay": 1, "stone": 2}]
        self.assertEqual(first_dict, second_dict)

    def test_whatMaterialColorBrown(self):
        self.assertEqual(whatMaterialColor("ore"), "brown")

    def test_whatMaterialColorGray(self):
        self.assertEqual(whatMaterialColor("loom"), "gray")

    def test_whatMaterialColorNA(self):
        self.assertEqual(whatMaterialColor("random"), "NA")