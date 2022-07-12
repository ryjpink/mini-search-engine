from typing import List, Tuple
from query import Disjunction, Query, Negation, Literal, Conjunction


def tokenize_query(text: str) -> List[str]:
    """Splits the text into query tokens (literals, keywords and punctuation)
    :param text: The query text
    :return: List of query tokens

    Example: "apple and ((cinnamon or cumin) and not orange) or pear)"
    => ['apple', 'and', '(', '(', 'cinnamon', 'or', 'cumin', ')', 'and', 'not', 'orange', ')', 'or', 'pear', ')']
    """
    result = []
    begin = 0
    end = 0
    while end < len(text):
        if text[end] == " ":
            if begin != end:
                result.append(text[begin:end])
            end += 1
            begin = end
        elif text[end] == "(" or text[end] == ")":
            if begin != end:
                result.append(text[begin:end])
            result.append(text[end])
            end += 1
            begin = end
        else:
            end += 1
    if begin != end:
        result.append(text[begin:end])
    return result


def is_literal(token: str) -> bool:
    return token not in {"and", "or", "not", "(", ")"}


def parse_factor(tokens: List[str], pos: int) -> Tuple[Query, int]:
    if pos == len(tokens):
        raise Exception("Unexpected end of factor")
    elif is_literal(tokens[pos]):
        return Literal(tokens[pos]), pos + 1
    elif tokens[pos] == "not":
        inner, pos = parse_factor(tokens, pos + 1)
        return Negation(inner), pos
    elif tokens[pos] == '(':
        inner, pos = parse_expression(tokens, pos + 1)
        if pos == len(tokens) or tokens[pos] != ')':
            raise Exception("Expected ')' after expression")
        return inner, pos + 1
    else:
        raise Exception(f"Unexpected token {tokens[pos]} while looking for factor")


def parse_term(tokens: List[str], pos: int) -> Tuple[Query, int]:
    factor, pos = parse_factor(tokens, pos)
    factors = [factor]
    while pos != len(tokens) and tokens[pos] == "and":
        factor, pos = parse_factor(tokens, pos + 1)
        factors.append(factor)
    return Conjunction(factors) if len(factors) > 1 else factors[0], pos


def parse_expression(tokens: List[str], pos: int = 0) -> Tuple[Query, int]:
    if pos == len(tokens):
        raise Exception("Unexpected end of expression")
    term, pos = parse_term(tokens, pos)
    if pos == len(tokens):
        return term, pos
    terms = [term]
    while pos != len(tokens) and tokens[pos] == "or":
        term, pos = parse_term(tokens, pos + 1)
        terms.append(term)
    return Disjunction(terms) if len(terms) > 1 else terms[0], pos


# "apple and ((cinnamon or cumin) and not orange) or pear)"
def parse_query(text: str) -> Query:
    tokens = tokenize_query(text)
    query, pos = parse_expression(tokens)
    if pos != len(tokens):
        raise Exception(f"Expected end of expression but found {tokens[pos]}")
    return query
