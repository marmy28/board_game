from wonder import Wonder


class Board(object):
    """

    """
    def __init__(self, parameters, cur):
        """Initializes the Board class. Sets the parameters such as name, side, etc. This class contains
        Wonders, your materials, and your split materials.

        :param parameters: Information that comes from the database about the board.
        :type parameters: dict | tuple
        :param cur: Connection to database so the wonders correspond to the correct board.
        :type cur: sqlite3.Cursor

        """
        self.id = parameters['id']
        self.name = parameters['name']
        self.side = parameters['side']
        self.material = {'coin': 0, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 0
                         , 'glass': 0, 'loom': 0, 'papyrus': 0}
        self.newMaterial('coin', 3)
        self.newMaterial(parameters['material'])
        self.split_material = {}
        self.wonders = []

        cur.execute("SELECT * FROM vWonders WHERE nBoardsId = ?", (str(self.id),))

        wonder_cards = cur.fetchall()
        for wonder_card in wonder_cards:
            self.wonders.append(Wonder(wonder_card))

    def newMaterial(self, material_name, number_to_change=1):
        """Records the new material for you.

        :param material_name: Name of the material you are changing. Should be a key from self.material.
        :type material_name: str | unicode
        :param number_to_change: How many of that material you are giving (negative number)
        or receiving (positive number).
        :type number_to_change: int
        :rtype: None

        """
        if (self.material[material_name] + number_to_change) >= 0:
            self.material[material_name] += number_to_change
        else:
            raise Exception('Cannot do this transaction: insufficient funds')

    def newSplitMaterial(self, ability):
        """Adds to your split materials which is different than your normal materials since you can
        only use one or the other.

        :param ability: name of two materials. Ex. stone/wood.
        :type ability: str
        :rtype: None

        """
        i = len(self.split_material)
        material = ability.split("/")
        self.split_material[i] = {material[0]: 1, material[1]: 1}

