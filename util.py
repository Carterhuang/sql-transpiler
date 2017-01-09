def standardize_keyword(token):
    """ In returned result, all keywords are in upper case."""
    return token.upper()


def join_tokens(lst, token):
    """
    While joining each element in 'lst' with token,
    we want to make sure each word is separated
    with space.
    """
    _token = token.strip(' ')
    if _token == '':
        # token only has empty space(s) in it,
        # we make standardize it to be one empty space.
        _token = ' '
    else:
        # Paddle a space on the left and right side of the token,
        # so that "AND" becomes " AND ".
        _token = ''.join([' ', standardize_keyword(_token), ' '])
    return _token.join(map(str, lst))


def normalize_keyword(input_str):
    """
    During transpiling, all reserved keywords(operators,
    macro/field headers, etc) are converted to lower case.
    e.g. 'AND' -> 'and', 'OR' -> 'or', etc.
    """
    return input_str.lower()


