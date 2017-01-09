from generate_sql import generate_sql

field_map = {
    1 : 'id',
    2 : 'name',
    3 : 'date_joined',
    4 : 'age'
}

macro_map = {
    "is_joe": ["=", ["field", 2], "joe"],
    "over_100": ['AND', ['!=', ['field', 2], None], ['=', ['field', 1], 100]]
}


example_input_1 = ["=", ["field", 2], "joe"]
print 'Example 1 output: ', generate_sql(field_map, example_input_1)

example_input_2 = ["AND", ["<", ["field", 1],  5], ["=", ["field", 2], "joe"]]
print 'Example 2 output: ', generate_sql(field_map, example_input_2)

example_input_3 = ["AND", ["<", ["field", 1],  5], ["macro", "is_joe"]]
print 'Example 3 output: ', generate_sql(field_map, example_input_3, macro_map)

