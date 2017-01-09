from transpile import transpile_simple_clause, transpile_compound_clause
from entity import Entity
from constants import *
from exception import TranspilerError

def generate_sql(field_map, input_data, macro_map={}):
    """
    This is method to be call for transpiling SQL query.
    e.g. generate_sql({1 : 'name'}, ['!=', ['field', 1], None]))
    shoud return SELECT * FROM data WHERE name IS NOT NULL.

    For bonus point, you may pass in a macro map as well.
    If that is the case, please specify macro id in the input
    data, do it like ['macro' : 'is_joe'].

    :type field_map: dict
    :type input_data: list
    :type macro_map: dict
    :rtype: str
    """
    if input_data == []:
        return SQL_HEADER

    entity = Entity(input_data)

    where_clause = ''
    if entity.is_simple_clause():
        where_clause = transpile_simple_clause(field_map, entity, macro_map)
    elif entity.is_compound_clause():
        where_clause = transpile_compound_clause(field_map, entity, macro_map)
    elif entity.is_macro():
        where_clause = transpile_macro(field_map, entity, macro_map)
    else:
        raise TranspilerError("Input (%s) not recognized." % (input_data))

    return SQL_HEADER + ' WHERE '+ where_clause

