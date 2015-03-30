class Card(object):
    """

    """
    def __init__(self, parameters):
        """Initializes the card variables like name, color, ability, etc.

        :param parameters: List that comes from the database full on information.
        :type parameters: dict | tuple
        :rtype: None

        """
        self.id = parameters['id']
        self.name = parameters['name']
        self.color = parameters['color']
        self.age = parameters['age']
        self.number_of_players = parameters['number_of_players']
        self.cost = {'coin': parameters['coin'], 'clay': parameters['clay'], 'ore': parameters['ore']
                     , 'stone': parameters['stone'], 'wood': parameters['wood'], 'glass': parameters['glass']
                     , 'loom': parameters['loom'], 'papyrus': parameters['papyrus']}
        self.free_from = parameters['free_from']
        self.ability = parameters['ability']
        self.give_free = parameters['give_free']
        self.trading_cost = {'left': 0, 'right': 0}

    def makeFree(self):
        """Makes the card free by setting the cost and trading cost to zero.

        :rtype: None

        """
        self.cost = {'coin': 0, 'clay': 0, 'ore': 0, 'stone': 0, 'wood': 0, 'glass': 0, 'loom': 0
                     , 'papyrus': 0}
        self.trading_cost = {'left': 0, 'right': 0}

    def totalCost(self):
        """Calculates the total coin cost of the card, including trading.

        :rtype: int

        """
        return self.cost['coin'] + self.trading_cost['left'] + self.trading_cost['right']

    def isFree(self):
        """Tells you whether or not the coin cost is zero.

        :rtype: bool

        """
        return self.totalCost() == 0