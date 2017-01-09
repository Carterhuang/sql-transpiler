from exception import TranspilerError
from constants import *

class Entity(object):
    def __init__(self, item):
        self.__item = item


    def is_literal_value(self):
        return type(self.__item) is not list


    def is_field_value(self):
        item = self.__item
        return type(item) is list and item[HEADER] == FIELD_HEADER


    def is_macro(self):
        item = self.__item
        return type(item) is list and item[HEADER] == MACRO_HEADER


    def is_clause(self):
        item = self.__item
        return type(item) is list and item[HEADER] in OPERATORS


    def is_single_clause(self):
        item = self.__item
        return type(item) is list and \
            (item[HEADER] in NON_CONJUNCTION  or item[HEADER] == MACRO_HEADER)


    def is_compound_clause(self):
        item = self.__item
        return type(item) is list and item[HEADER] in CONJUNCTION


    def __validate_literal_value(self):
        if not self.is_literal_value():
            raise TranspilerError("Not a literal value entity: %s!" % (self.__item))


    def __validate_field_value(self):
        if not self.is_field_value():
            raise TranspilerError("Not a field value entity: %s!" % (self.__item))


    def __validate_clause(self):
        if not self.is_clause():
            raise TranspilerError("Not a clause entity: %s!" % (self.__item))


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


    def get_operator(self):
        self.__validate_clause();
        return self.__item[HEADER]


    def get_arguments(self):
        self.__validate_clause()
        return map(lambda item: Entity(item), self.__item[PARAMS:])


    def __str__(self):
        return str(self.__item)










