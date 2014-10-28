__author__ = 'Matthew Armbruster'


def compareDicts(my_dict):
    intCounter = 0
    while intCounter < len(my_dict) - 1:
        intCounter2 = intCounter + 1
        while intCounter2 < len(my_dict):
            if my_dict[intCounter].keys() == my_dict[intCounter2].keys() \
                    and my_dict[intCounter].values() == my_dict[intCounter2].values():
                my_dict.pop(intCounter2)
            else:
                intCounter2 += 1
        intCounter += 1


def whatMaterialColor(materialName):
    if materialName in ("wood", "ore", "stone", "clay"):
        return "brown"
    elif materialName in ("glass", "papyrus", "loom"):
        return "gray"
    else:
        return "NA"


def getScienceScore(science):
    score = min(science.values()) * 7
    for i in science.values():
        score += i ** 2
    return score


def makeSureArray(func):
    def checker(make_array, args):
        if type(make_array) == dict:
            new_array = [make_array.copy()]
        else:
            new_array = make_array
        ret = func(new_array, args)
        return ret
    return checker


def sortDict(func):
    def checker(unsorted_dict):
        sorted_dict = sorted(unsorted_dict, key=len)
        ret = func(sorted_dict)
        return ret
    return checker


@makeSureArray
def buyWithSplit(cost_copy, split_mat):
    for key, sp_mat in split_mat.items():
        my_length = len(cost_copy)
        trigger = [False]*my_length
        for mat, amount in sp_mat.items():
            i = 0
            while i < my_length:
                if cost_copy[i].has_key(mat) and amount > 0:
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
            for k, v in option.items():
                if v >= 0:
                    option.pop(k)

            if len(option) == 0:
                return True

    return cost_copy

@sortDict
def eraseMoreExpensive(card_cost):
    # card_cost = sorted(card_cost, key=len)
    intCounter = 0
    while intCounter < len(card_cost) - 1:
        intCounter2 = intCounter + 1
        while intCounter2 < len(card_cost):
            j = 0
            for i in card_cost[intCounter].keys():
                if card_cost[intCounter2].has_key(i):
                    if card_cost[intCounter][i] >= card_cost[intCounter2][i]:
                        j += 1
            if j == len(card_cost[intCounter].keys()):
                card_cost.pop(intCounter2)
            else:
                intCounter2 += 1
        intCounter += 1
    return card_cost


def canBuyThroughTrade(needed_materials, trade_cost, neighbors_materials):
    """This will send back the trading and modify the needed_materials...only for non-split materials"""
    material_to_money = []
    for mat_options in needed_materials:
        spend_to_trade = 0
        for mat, amount in mat_options.items():
            if neighbors_materials.has_key(mat):
                if neighbors_materials[mat] >= abs(amount):
                    spend_to_trade += (abs(amount)*trade_cost[whatMaterialColor(mat)])
                    mat_options.pop(mat)
                elif neighbors_materials[mat] > 0:
                    spend_to_trade += ((abs(amount) - neighbors_materials[mat])*trade_cost[whatMaterialColor(mat)])
                    mat_options[mat] += neighbors_materials[mat]
        material_to_money.append(spend_to_trade)

    return material_to_money


def exterminateTooExpensiveOrGray(trading_cost, card_cost, mat_array, coin_have, check_gray=True):
    """ Takes out too expensive costs...do this before look at split materials"""
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
    for key, sp_mat in split_mat.items():
        my_length = len(cost)
        trigger = [False]*my_length
        for mat, amount in sp_mat.items():
            i = 0
            while i < my_length:
                if cost[i].has_key(mat) and amount > 0 > cost[i][mat]:
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
            for k, v in option.items():
                if v >= 0:
                    option.pop(k)


def expelExtraMaterial(coin_cost, materials):
    i = 0
    while i < len(materials):
        if len(materials[i]) != 0:
            materials.pop(i)
            coin_cost['right'].pop(i)
            coin_cost['left'].pop(i)
        else:
            i += 1


def findCheapestTrade(trading_cost):
    i = 0
    cheapest = trading_cost['right'][i] + trading_cost['left'][i]
    cheapestDict = {'right': trading_cost['right'][i], 'left': trading_cost['left'][i]}
    while i < len(trading_cost['right']):
        if (trading_cost['right'][i] + trading_cost['left'][i]) < cheapest:
            cheapestDict = {'right': trading_cost['right'][i], 'left': trading_cost['left'][i]}
        i += 1
    return cheapestDict