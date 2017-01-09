import unittest
from generate_sql import generate_sql

class GenerateSQLRegressionTestCase(unittest.TestCase):

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


    def test_transpile_nested_statement(self):
        input_data = ["AND", ["!=", ["field", 3], None], ["OR", [">", ["field", 4], 25],
         ["=", ["field", 2], "Jerry"]]]

        self.assertEqual(
            generate_sql(self.field_map, input_data),
            "SELECT * FROM data WHERE date_joined IS NOT NULL AND (age > 25 OR name = 'Jerry')"
        )


    def test_transpile_statement_with_macro(self):
        input_data = ["AND", ["<", ["field", 1],  5], ["macro", "is_joe"]]

        self.assertEqual(
            generate_sql(self.field_map, input_data, self.macro_map),
            "SELECT * FROM data WHERE id < 5 AND name = 'joe'"
        )
