from exception import TranspilerError
from constants import *

"""
In this transpiler implementation, every non-operator item is
wrapped up as an "entity".
For example,
    * ["field", 1] is a field entity;
    * literals such as 100,  "joe" are literal entities;
    * ["macro", 1] is a macro entity;
    * ["<", ["field", 1], 5] is a single clause entity;
    * ["AND", <clause_1>, <clause_2>] is a compound entity;
"""

class Entity(object):
    def __init__(self, item):
        self.__item = item


    def is_literal_value(self):
        """
        e.g. 'joe', 1, None, 99.99, etc; in this implementation
        as long as it is not a list type object.
        """
        return type(self.__item) is not list


    def is_field_value(self):
        """
        e.g. ["field", 1]
        """
        item = self.__item
        return type(item) is list and item[HEADER] == FIELD_HEADER


    def is_macro(self):
        """
        e.g. ["macro", "is_joe"] while "is_joe" points to the
        macro in the macro map.
        """
        item = self.__item
        return type(item) is list and item[HEADER] == MACRO_HEADER


    def is_clause(self):
        """
        simple or compound clause which contributes to 'where'
        statement in the SQL query.
        """
        item = self.__item
        return type(item) is list and item[HEADER] in OPERATORS


    def is_simple_clause(self):
        """
        e.g. ['<', ['field', 1], 25]
        """
        item = self.__item
        return type(item) is list and item[HEADER] in NON_CONJUNCTION


    def is_compound_clause(self):
        """
        format: [<operator>, <clause_1>, <clause_2> ... ]
        """
        item = self.__item
        return type(item) is list and item[HEADER] in CONJUNCTION


    def __validate_clause(self):
        if not self.is_clause():
            raise TranspilerError("Not a clause entity: %s!" % (self.__item))


    def __validate_literal_value(self):
        if not self.is_literal_value():
            raise TranspilerError("Not a literal value entity: %s!" % (self.__item))


    def __validate_field_value(self):
        if not self.is_field_value():
            raise TranspilerError("Not a field value entity: %s!" % (self.__item))


    def __validate_macro(self):
        if not self.is_macro():
            raise TranspilerError("Not a macro: %s" % (self.i__item))


    def get_literal_value(self):
        self.__validate_literal_value()
        return self.__item


    def get_field_id(self):
        self.__validate_field_value()
        field_header, field_id = self.__item
        return field_id


    def get_macro_id(self):
        self.__validate_macro()
        macro_header, macro_id = self.__item
        return macro_id

    """
    A clause entity is made up of an operator, and arguments.
    For example, for clause like ['>', ['field', 1], 25], the operator
    is '>' while the arguments are ['field', 1] (a field entity), and
    25 (a literal entityf).
    """

    def get_operator(self):
        self.__validate_clause();
        return self.__item[HEADER]


    def get_arguments(self):
        """
        Each argument is returned as an entity.
        """
        self.__validate_clause()
        return map(lambda item: Entity(item), self.__item[PARAMS:])


    def __str__(self):
        return str(self.__item)

