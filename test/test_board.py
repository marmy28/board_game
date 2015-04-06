from unittest import TestCase
import sqlite3
from board import Board


class TestBoard(TestCase):

    def setUp(self):
        con = sqlite3.connect("../database.db")
        con.row_factory = sqlite3.Row
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM vBoards WHERE id = 1")
            self.board_olympia = Board(cur.fetchone(), cur)
        con.close()

    def test_setUp(self):
        self.assertEqual(self.board_olympia.id, 1)
        self.assertEqual(self.board_olympia.name, "olympia")
        self.assertEqual(self.board_olympia.side, "a")

    def test_newMaterial_NewMaterialAdd1(self):
        expect = {'coin': 3, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 1,
                  'glass': 1, 'loom': 0, 'papyrus': 0}
        self.board_olympia.newMaterial("glass")
        self.assertDictEqual(self.board_olympia.material, expect)

    def test_newMaterial_NewMaterialAdd2(self):
        expect = {'coin': 3, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 1,
                  'glass': 2, 'loom': 0, 'papyrus': 0}
        self.board_olympia.newMaterial("glass", 2)
        self.assertDictEqual(self.board_olympia.material, expect)

    def test_newMaterial_NewMaterialSubtract1(self):
        expect = {'coin': 2, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 1,
                  'glass': 0, 'loom': 0, 'papyrus': 0}
        self.board_olympia.newMaterial("coin", -1)
        self.assertDictEqual(self.board_olympia.material, expect)

    def test_newMaterial_RaiseException(self):
        with self.assertRaises(Exception):
            self.board_olympia.newMaterial("coin", -4)

    def test_newSplitMaterial(self):
        expect = {0: {"wood": 1, "stone": 1}}
        self.board_olympia.newSplitMaterial("wood/stone")
        self.assertDictEqual(self.board_olympia.split_material, expect)