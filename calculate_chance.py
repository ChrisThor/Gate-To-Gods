def calculate_chance(rng, value_limit) -> bool:
    """
    This function calculates a float between 1 and 100000001. If the calculated value is smaller or equal to
    "value_limit", True is returned, otherwise False.
    :param rng:         The rng object
    :param value_limit:
    :return:            True or False
    """
    val = rng.randrange(1, 100000001) / 100000000
    if val <= value_limit:
        return True
    return False
