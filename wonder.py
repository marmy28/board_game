class Wonder(object):
    """

    """
    def __init__(self, parameters):
        """Initializes the wonders for your specific board. Very similar to Card(object).

        :param parameters: Information about the specific wonder from the database.
        :type parameters: dict | tuple
        :rtype: None

        """
        self.name = str(parameters['name'])
        self.color = parameters['color'].split(" & ")
        self.cost = {'coin': parameters['coin'], 'clay': parameters['clay'], 'ore': parameters['ore']
                     , 'stone': parameters['stone'], 'wood': parameters['wood'], 'glass': parameters['glass']
                     , 'loom': parameters['loom'], 'papyrus': parameters['papyrus']}
        self.ability = parameters['ability'].split(" & ")
        self.trading_cost = {'left': 0, 'right': 0}

    def resetTrade(self):
        """Sets the coin amount for trading back to zero for each side.

        :rtype: None

        """
        self.trading_cost = {'left': 0, 'right': 0}

    def wonderTotalCost(self):
        """The total coin cost of the wonder, including trading.

        :rtype: int

        """
        return self.trading_cost['left'] + self.trading_cost['right'] + self.cost['coin']