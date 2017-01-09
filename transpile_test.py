import unittest
from entity import Entity
from transpile import *

class SingleClauseTestCase(unittest.TestCase):

    def setUp(self):
        self.field_map = {
            1 : 'id',
            2 : 'name',
            3 : 'date_joined',
            4 : 'age'
        }

        self.macro_map = {
            "is_joe": ["=", ["field", 2], "joe"]
        }

    def test_transpile_string_literal(self):
        entity = Entity('string')
        self.assertEqual(transpile_literal(entity), "\'string\'")


    def test_transpile_non_string_literal(self):
        entity = Entity(123)
        self.assertEqual(transpile_literal(entity), '123')


    def test_transpile_is_empty(self):
        entity = Entity(['field', 2])
        self.assertEqual(transpile_is_empty(self.field_map, entity), 'name IS NULL')


    def test_transpile_not_empty(self):
        entity = Entity(['field', 4])
        self.assertEqual(transpile_not_empty(self.field_map, entity), 'age IS NOT NULL')


    def test_transpile_comparison_number(self):
        operator, field_entity, literal_entity = '>', Entity(['field', 4]), Entity(25)
        self.assertEqual(
            transpile_comparison(self.field_map, operator, field_entity, literal_entity),
            'age > 25'
        )


    def test_transpile_comparison_string(self):
        operator, field_entity, literal_entity = '!=', Entity(['field', 2]), Entity('Carter')
        self.assertEqual(
            transpile_comparison(self.field_map, operator, field_entity, literal_entity),
            "name <> 'Carter'"
        )


    def test_transpile_comparison_not_null(self):
        operator, field_entity, literal_entity = '!=', Entity(['field', 2]), Entity(None)
        self.assertEqual(
            transpile_comparison(self.field_map, operator, field_entity, literal_entity),
            "name IS NOT NULL"
        )


    def test_transpile_comparison_is_null(self):
        operator, field_entity, literal_entity = '=', Entity(['field', 2]), Entity(None)
        self.assertEqual(
            transpile_comparison(self.field_map, operator, field_entity, literal_entity),
            "name IS NULL"
        )


    def test_transpile_simple_clause_equal(self):
        clause_entity = Entity(['=', ['field', 3], None])

        self.assertEqual(
            transpile_simple_clause(self.field_map, clause_entity),
            "date_joined IS NULL"
        )


    def test_transpile_simple_clause_greater(self):
        clause_entity = Entity(['>', ['field', 4], 35])

        self.assertEqual(
            transpile_simple_clause(self.field_map, clause_entity),
            "age > 35"
        )


    def test_transpile_compound_clause_basic(self):
        clause_entity = Entity(["AND", ["<", ["field", 1],  5], ["=", ["field", 2], "joe"]])

        self.assertEqual(
            transpile_compound_clause(self.field_map, clause_entity),
            "id < 5 AND name = 'joe'"
        )


    def test_transpile_compound_clause_simple(self):
        clause_entity = Entity(["OR", ["!=", ["field", 3], "2015-11-01"], ["=", ["field", 1], 456]])

        self.assertEqual(
            transpile_compound_clause(self.field_map, clause_entity),
            "date_joined <> '2015-11-01' OR id = 456"
        )


    def test_transpile_compound_clause_nested(self):
        clause_entity = Entity(["AND", ["!=", ["field", 3], None], ["OR", [">", ["field", 4], 25],
         ["=", ["field", 2], "Jerry"]]])

        self.assertEqual(
            transpile_compound_clause(self.field_map, clause_entity),
            "date_joined IS NOT NULL AND (age > 25 OR name = 'Jerry')"
        )


    def test_transpile_compound_with_macro(self):
        clause_entity = Entity(["AND", ["<", ["field", 1],  5], ["macro", "is_joe"]])

        self.assertEqual(
            transpile_compound_clause(self.field_map, clause_entity, self.macro_map),
            "id < 5 AND name = 'joe'"
        )






