import unittest

from parser import tokenize_query, parse_query
from query import Query


class TokenizerTest(unittest.TestCase):

    def test_simple_query(self):
        tokens = tokenize_query('apple and orange')
        self.assertEqual(tokens, ['apple', 'and', 'orange'])

    def test_spaces(self):
        tokens = tokenize_query('  apple and(  orange )  ')
        self.assertEqual(tokens, ['apple', 'and', '(', 'orange', ')'])

    def test_complex_query(self):
        tokens = tokenize_query('apple and ((cinnamon or cumin) and not orange) or pear)')
        self.assertEqual(tokens, ['apple', 'and', '(', '(', 'cinnamon', 'or', 'cumin', ')', 'and', 'not', 'orange', ')', 'or', 'pear', ')'])


class QueryParserTest(unittest.TestCase):
    def test_complex_query(self):
        query = parse_query("apple and (cinnamon or cumin) and (not orange) or pear")
        self.assertIsInstance(query, Query)
        self.assertEqual(str(query), "((apple and (cinnamon or cumin) and (not orange)) or pear)")

    def test_simple_query(self):
        query = parse_query("apple and pear")
        self.assertIsInstance(query, Query)
        self.assertEqual(str(query), "(apple and pear)")

    def test_negation_query(self):
        query = parse_query("not apple and pear")
        self.assertIsInstance(query, Query)
        self.assertEqual(str(query), "((not apple) and pear)")


