from constants import *
from exception import TranspilerError

SPACE = ' '

"""
Session for transpiling field and literals.
"""

def transpile_literal(literal_entity):
    literal = literal_entity.get_literal_value()
    value_type = type(literal)

    if value_type is str:
        return "\'%s\'" % (literal)
    elif value_type is type(None):
        return 'NULL'
    else:
        return str(literal)


def transpile_field(field_map, field_entity):
    field_id = field_entity.get_field_id()

    if field_id not in field_map:
        raise TranspilerError("Field id (%s) does not exist." % (field_id))

    return field_map.get(field_id)


"""
Session for transpiling non-conjuction operators.
"""
def join_tokens(lst, token):
    _token = token.strip(' ')
    if _token == '':
        _token = ' '
    else:
        # Paddle a space on the left and right side of the token.
        _token = ''.join([' ', _token, ' '])
    return _token.join(map(str, lst))

def transpile_is_empty(field_map, field_entity):
    field = transpile_field(field_map, field_entity)
    return  join_tokens([field, 'IS NULL'], SPACE)


def transpile_not_empty(field_map, field_entity):
    field = transpile_field(field_map, field_entity)
    return join_tokens([field, 'IS NOT NULL'], SPACE)


def transpile_not_equal(field_map, field_entity, literal_entity):
    field = transpile_field(field_map, field_entity)
    literal = transpile_literal(literal_entity)
    return join_tokens([field, '<>', literal], SPACE)


def transpile_comparison(field_map, operator, field_entity, literal_entity):
    literal = literal_entity.get_literal_value()

    if literal == None  and operator in ['=', '!=']:
        return {
            '=' : lambda fm, fe: transpile_is_empty(fm, fe),
            '!=' : lambda fm, fe: transpile_not_empty(fm, fe)
        } [operator] (field_map, field_entity)
    elif operator == '!=':
        return transpile_not_equal(field_map, field_entity, literal_entity)
    else:
        transpiled_field = transpile_field(field_map, field_entity)
        transpiled_literal = transpile_literal(literal_entity)

        return join_tokens([transpiled_field, operator, transpiled_literal], SPACE)


"""
Transpile the whole single clause.
"""

def transpile_single_clause(field_map, clause_entity):
    if not clause_entity.is_single_clause():
        raise TranspilerError("Clause (%s) is not a single clause." % (clause_entity))

    operator = clause_entity.get_operator()
    params = clause_entity.get_arguments()

    if operator in ['is_empty', 'not_empty']:
        field_entity = params[0]
        return {
            'is_empty' : lambda m, f: transpile_is_empty(m, f),
            'not_empty' : lambda m, f: transpile_not_empty(m, f)
        } [operator] (field_map, field_entity)
    else:
        # When it is a normal arithmatic comparison operator.
        field_entity, literal_entity = params
        return transpile_comparison(field_map, operator, field_entity, literal_entity)


"""
Transpile compound clause.
"""

def transpile_compound_clause(field_map, clause_entity):
    if not clause_entity.is_compound_clause():
        raise TranspilerError("Clause (%s) is not a compound clause." % (clause))

    operator = clause_entity.get_operator()
    clauses = clause_entity.get_arguments()

    add_paranthesis_if_compound = lambda clause: \
    '(' + transpile_compound_clause(field_map, clause) + ')' \
    if clause.is_compound_clause() else transpile_single_clause(field_map, clause)

    return join_tokens(map(add_paranthesis_if_compound, clauses), operator)

