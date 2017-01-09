from transpile import transpile_single_clause, transpile_compound_clause
from entity import Entity
from constants import *


def generate_sql(field_map, input_data, macro_map={}):
    entity = Entity(input_data)

    where_clause = ''
    if entity.is_single_clause():
        where_clause = transpile_single_clause(field_map, entity, macro_map)
    elif entity.is_compound_clause():
        where_clause = transpile_compound_clause(field_map, entity, macro_map)
    elif entity.is_macro():
        where_clause = transpile_macro(field_map, entity, macro_map)
    else:
        raise TranspileError("Input (%s) not recognized." % (input_data))

    return SQL_HEADER + ' '+ where_clause

