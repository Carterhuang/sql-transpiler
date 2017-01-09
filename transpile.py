from exception import TranspilerError
from entity import Entity
from util import join_tokens

SPACE = ' '

"""
This file includes the core logic for transpilation. It maps
each input data to the "where" portion of the SQL query.
"""

"""
* Session for transpiling field and literals.
"""

def transpile_literal(literal_entity):
    literal = literal_entity.get_literal_value()
    value_type = type(literal)

    if value_type is str:
        # If literal is a string, quote it.
        return "\'%s\'" % (literal)
    elif value_type is type(None):
        return 'NULL'
    else:
        return str(literal)


def transpile_field(field_map, field_entity):
    """ Map field id to column name in the field_map """
    field_id = field_entity.get_field_id()

    if field_id not in field_map:
        raise TranspilerError("Field id (%s) does not exist." % (field_id))

    return field_map.get(field_id)


"""
* Session for transpiling non-conjuction operators.
"""

def transpile_is_empty(field_map, field_entity):
    """ transpiling 'is_empty' statement """
    field = transpile_field(field_map, field_entity)
    return  join_tokens([field, 'IS NULL'], SPACE)


def transpile_not_empty(field_map, field_entity):
    """ transpiling 'not_empty' statement """
    field = transpile_field(field_map, field_entity)
    return join_tokens([field, 'IS NOT NULL'], SPACE)


def transpile_not_equal(field_map, field_entity, literal_entity):
    """ ['!=', ['field' : 2], 25] -> age <> 25 """
    field = transpile_field(field_map, field_entity)
    literal = transpile_literal(literal_entity)
    return join_tokens([field, '<>', literal], SPACE)


def transpile_comparison(field_map, operator, field_entity, literal_entity):
    literal = literal_entity.get_literal_value()

    if literal == None  and operator in ['=', '!=']:
        # This if statement transpile "<arg> != None"
        # and "<arg> == None" to "<arg> IS NOT NULL"
        # or "<arg> IS NULL".
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
* Section for transpiling simple clause.
"""

def transpile_simple_clause(field_map, clause_entity, macro_map={}):
    """
    Transpile the whole simple clause.
    """
    if not clause_entity.is_simple_clause():
        raise TranspilerError("Clause (%s) is not a simple clause." % (clause_entity))
    else:
        operator = clause_entity.get_operator()
        arguments = clause_entity.get_arguments()

        if operator in ['is_empty', 'not_empty']:
            field_entity = arguments[0]
            return {
                'is_empty' : lambda m, f: transpile_is_empty(m, f),
                'not_empty' : lambda m, f: transpile_not_empty(m, f)
            } [operator] (field_map, field_entity)
        else:
            # It is simple clause with one operator and two arguments, follows
            # [<operator>, <field>, <literal>] format.
            field_entity, literal_entity = arguments
            return transpile_comparison(field_map, operator, field_entity, literal_entity)



def transpile_compound_clause(field_map, clause_entity, macro_map={}, subclause=False):
    """
    Transpile compound clause.
    subclause parameter indicates whether this compound clause is
    a sub clause of another compound clause.
    """
    if not clause_entity.is_compound_clause():
        raise TranspilerError("Clause (%s) is not a compound clause." % (clause))

    operator = clause_entity.get_operator()
    entities = clause_entity.get_arguments()

    transpiled_entities = []

    # Each sub entity can either be a simple clause, compound clause or macro.
    # If it is a compound clause, then it needs to be wrapped in a pair of
    # parenthesis.
    for sub_entity in entities:
        if sub_entity.is_simple_clause():
            transpiled_entities.append(transpile_simple_clause(field_map, sub_entity))
        elif sub_entity.is_compound_clause():
            transpiled_entities.append(transpile_compound_clause(field_map, sub_entity, subclause=True))
        elif sub_entity.is_macro():
            transpiled_entities.append(transpile_macro(field_map, sub_entity, macro_map, subclause=True))
        else:
            raise TranspilerError('Entity (%s) should be a clause but it is not.' % (sub_entity))

    transpiled_compound_clause = join_tokens(transpiled_entities, operator)

    # If the input compound clause is a subclause of another compound clause, then we wrap it up
    # with '()'.
    return '(' + transpiled_compound_clause + ')' if subclause else transpiled_compound_clause



def transpile_macro(field_map, macro_entity, macro_map={}, subclause=False):
    """
    Transpile macro entity.
    """
    macro_id = macro_entity.get_macro_id()

    if macro_id not in macro_map:
        raise TranspilerError("Macro id: (%s) does not exist." % (macro_id))

    entity = Entity(macro_map[macro_id])

    if entity.is_macro():
        # This takes care of one macro point to another macro, which
        # is weird, but possible.
        return transpile_macro(field_map, entity, macro_map)
    elif entity.is_simple_clause():
        return transpile_simple_clause(field_map, entity, macro_map)
    elif entity.is_compound_clause():
        return transpile_compound_clause(field_map, entity, macro_map, subclause=subclause)
    else:
        raise TranspilerError('Macro entity (%s) not recognized.' % (entity))
