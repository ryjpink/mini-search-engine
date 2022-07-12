import unittest
from query import Conjunction, Literal, Disjunction, Negation


class QueryTreeTest(unittest.TestCase):

    def test_print(self):
        root = Conjunction([
            Literal('apple'),
            Disjunction([
                Literal('cinnamon'),
                Literal('pear')]),
            Negation(Literal('orange'))])
        self.assertEqual(str(root), '(apple and (cinnamon or pear) and (not orange))')

    def test_literal(self):
        root = Literal('apple')
        self.assertEqual(str(root), 'apple')

    def test_negation(self):
        root = Negation(Literal('apple'))
        self.assertEqual(str(root), '(not apple)')

    def test_conjunction(self):
        root = Conjunction([Literal('apple'), Literal('kiwi')])
        self.assertEqual(str(root), '(apple and kiwi)')

    def test_disjunction(self):
        root = Disjunction([Literal('apple'), Literal('kiwi')])
        self.assertEqual(str(root), '(apple or kiwi)')
