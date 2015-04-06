#####################
#### Decorators #####
#####################


def makeSureArray(func):
    """Decorator that makes sure the function gets an array of dictionaries.
    """
    def checker(make_array, args):
        if isinstance(make_array, dict):
            new_array = [make_array.copy()]
        else:
            new_array = make_array
        ret = func(new_array, args)
        return ret
    return checker


def sortDict(func):
    """Decorator that sorts the dictionary by length before it goes into the function.
    """
    def checker(unsorted_dict):
        sorted_dict = sorted(unsorted_dict, key=len)
        ret = func(sorted_dict)
        return ret
    return checker
    
#####################
#### Functions ######
#####################


def compareDicts(my_dict):
    """Compares dictionaries and gets rid of duplicate cases.

    :param my_dict: Array of dictionaries.
    :type my_dict: list
    :rtype: None
    """
    i = 0
    while i < len(my_dict) - 1:
        j = i + 1
        while j < len(my_dict):
            if my_dict[i] == my_dict[j]:
                my_dict.pop(j)
            else:
                j += 1
        i += 1


def whatMaterialColor(material_name):
    """Tells if the material is a certain color.

    :param material_name: str
    :rtype: str
    """
    if material_name in ("wood", "ore", "stone", "clay"):
        return "brown"
    elif material_name in ("glass", "papyrus", "loom"):
        return "gray"
    else:
        return "NA"


def getScienceScore(science):
    """Calculates the science score.

    :param science: Tells how many of each science the player has.
    :type science: dict
    :rtype: int
    """
    score = min(science.values()) * 7
    for i in science.values():
        score += i ** 2
    return score


@makeSureArray
def buyWithSplit(cost_copy, split_mat):
    """Returns whether you can buy a card or wonder with the split materials given or what else is
    required before you can buy it.

    :param cost_copy: The cost of the card.
    :type cost_copy: list | dict
    :param split_mat: The split materials available.
    :type split_mat: dict
    :rtype: bool | dict
    """
    for key, sp_mat in split_mat.items():
        my_length = len(cost_copy)
        trigger = [False]*my_length
        for mat, amount in sp_mat.items():
            i = 0
            while i < my_length:
                if (mat in cost_copy[i]) and amount > 0:
                    cost_copy.append(cost_copy[i].copy())
                    cost_copy[-1][mat] += amount
                    trigger[i] = True
                i += 1
        i = 0
        while i < len(trigger):
            if trigger[i]:
                cost_copy.pop(i)
                trigger.pop(i)
            else:
                i += 1

        for option in cost_copy:
            duplicate_option = option.copy()
            for k, v in duplicate_option.items():
                if v >= 0:
                    option.pop(k)

            if not option:
                return True

    return cost_copy

@sortDict
def eraseMoreExpensive(card_cost):
    """Erases the more expensive cards for example if you either need 1 wood or 1 wood and 1 clay
    this function will get rid of the 1 wood and 1 clay option since it will cost more.

    :param card_cost: Material still needed to buy the card or wonder.
    :type card_cost: list
    :rtype: list
    """
    counter = 0
    while counter < len(card_cost) - 1:
        another_counter = counter + 1
        while another_counter < len(card_cost):
            j = 0
            for i in card_cost[counter].keys():
                if i in card_cost[another_counter]:
                    if card_cost[counter][i] >= card_cost[another_counter][i]:
                        j += 1
            if j == len(card_cost[counter].keys()):
                card_cost.pop(another_counter)
            else:
                another_counter += 1
        counter += 1
    return card_cost


def canBuyThroughTrade(needed_materials, trade_cost, neighbors_materials):
    """This will send back the trading and modify the needed_materials...only for non-split materials.

    :param needed_materials: List of needed materials to buy the card or wonder.
    :type needed_materials: dict | list
    :param trade_cost: How much it costs to trade with each neighbor.
    :type trade_cost: dict
    :param neighbors_materials: Your neighbor's materials.
    :type neighbors_materials: dict
    :rtype: list
    """
    material_to_money = []
    for mat_options in needed_materials:
        spend_to_trade = 0
        mat_options_copy = mat_options.copy()
        for mat, amount in mat_options_copy.items():
            if mat in neighbors_materials:
                if neighbors_materials[mat] >= abs(amount):
                    spend_to_trade += (abs(amount)*trade_cost[whatMaterialColor(mat)])
                    mat_options.pop(mat)
                elif neighbors_materials[mat] > 0:
                    spend_to_trade += ((abs(amount) - neighbors_materials[mat])*trade_cost[whatMaterialColor(mat)])
                    mat_options[mat] += neighbors_materials[mat]
        material_to_money.append(spend_to_trade)

    return material_to_money


def exterminateTooExpensiveOrGray(trading_cost, card_cost, mat_array, coin_have, check_gray=True):
    """ Takes out too expensive costs...do this before look at split materials.

    :param trading_cost: How much it costs to trade with each neighbor.
    :type trading_cost: dict
    :param card_cost: How much coin is needed to buy the card or wonder.
    :type card_cost: int
    :param mat_array: Materials needed to buy the card or wonder.
    :type mat_array: dict | list
    :param coin_have: The coin you have available to spend.
    :type coin_have: int
    :param check_gray: Whether or not to check for gray cards.
    :type check_gray: bool
    :rtype: None
    """
    i = 0
    while i < len(trading_cost['right']):
        if (trading_cost['right'][i] + trading_cost['left'][i] + card_cost) > coin_have:
            trading_cost['right'].pop(i)
            trading_cost['left'].pop(i)
            mat_array.pop(i)
        else:
            i += 1

    if check_gray:
        i = 0
        while i < len(mat_array):
            for material in mat_array[i].keys():
                if whatMaterialColor(material) == 'gray':
                    trading_cost['right'].pop(i)
                    trading_cost['left'].pop(i)
                    mat_array.pop(i)
                    i -= 1
                    break
            i += 1


def buyWithSplitTrade(cost, split_mat, trade_cost, coin_array, side):
    """Calculates how much it will cost to trade using the neighbor's split materials.

    :param cost: The needed materials to buy the card or wonder.
    :type cost: dict | list
    :param split_mat: Neighbor's split materials.
    :type split_mat: dict
    :param trade_cost: How much it costs to trade with your neighbor.
    :type trade_cost: dict
    :param coin_array: Possible combinations of coin trade cost.
    :type coin_array: dict
    :param side: Left or right
    :type side: str
    :rtype: None
    """
    for key, sp_mat in split_mat.items():
        my_length = len(cost)
        trigger = [False]*my_length
        for mat, amount in sp_mat.items():
            i = 0
            while i < my_length:
                if (mat in cost[i]) and amount > 0 > cost[i][mat]:
                    cost.append(cost[i].copy())
                    coin_array['right'].append(coin_array['right'][i])
                    coin_array['left'].append(coin_array['left'][i])
                    cost[-1][mat] += amount
                    coin_array[side][-1] += (abs(amount)*trade_cost[whatMaterialColor(mat)])
                    trigger[i] = True
                i += 1
        i = 0
        while i < len(trigger):
            if trigger[i]:
                cost.pop(i)
                coin_array['right'].pop(i)
                coin_array['left'].pop(i)
                trigger.pop(i)
            else:
                i += 1

        for option in cost:
            option_copy = option.copy()
            for k, v in option_copy.items():
                if v >= 0:
                    option.pop(k)


def expelExtraMaterial(coin_cost, materials):
    """Gets rid of the combinations to buy a card or wonder that still have materials left. This
    happens before you set how much it will cost.

    :param coin_cost: Possible cost of buying the card.
    :type coin_cost: dict
    :param materials: Materials left making it not possible to buy the card with this combination.
    :type materials: dict | list
    :rtype: None
    """
    i = 0
    while i < len(materials):
        if materials[i]:
            materials.pop(i)
            coin_cost['right'].pop(i)
            coin_cost['left'].pop(i)
        else:
            i += 1


def findCheapestTrade(trading_cost):
    """Finds the cheapest total cost for trading.

    :param trading_cost: How much it costs to buy the material to each the right and left neighbor.
    :type trading_cost: dict
    :rtype: dict
    """
    i = 0
    cheapest = trading_cost['right'][i] + trading_cost['left'][i]
    cheapest_dict = {'right': trading_cost['right'][i], 'left': trading_cost['left'][i]}
    while i < len(trading_cost['right']):
        if (trading_cost['right'][i] + trading_cost['left'][i]) < cheapest:
            cheapest_dict = {'right': trading_cost['right'][i], 'left': trading_cost['left'][i]}
        i += 1
    return cheapest_dict
