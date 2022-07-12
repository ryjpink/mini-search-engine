import heapq
from typing import List, Iterator, Dict
from posting_list import PostingList, DocId


class Cursor:
    head: DocId
    tail: Iterator[DocId]

    def __init__(self, tail: Iterator[DocId], head: DocId = -1):
        self.head = head
        self.tail = tail

    def __lt__(self, other):
        return self.head < other.head

    def __next__(self):
        return Cursor(self.tail, self.tail.__next__())

    def next_from(self, target: DocId):
        cur = self.tail.__next__()
        while cur < target:
            cur = self.tail.__next__()
        return Cursor(self.tail, cur)


class Query:
    def execute(self, posting_lists: Dict[str, PostingList]) -> Iterator[DocId]:
        raise Exception("unimplemented method")


class Literal(Query):
    # Example: "apple"
    term: str

    def __init__(self, term: str):
        self.term = term

    def __str__(self):
        return self.term

    def execute(self, posting_lists: Dict[str, PostingList]) -> Iterator[DocId]:
        if self.term in posting_lists:
            posting_list = posting_lists[self.term]
            for doc_id in posting_list:
                yield doc_id


class Conjunction(Query):
    # Example: "apple and pear"
    # "apple and pear and cinnamon"
    # "apple and (pear or cinnamon)"
    terms: List[Query]

    def __init__(self, terms: List[Query]):
        self.terms = terms

    def __str__(self):
        result = []
        for term in self.terms:
            if len(result) != 0:
                result.append('and')
            result.append(str(term))
        return f'({" ".join(result)})'

    def execute(self, posting_lists: Dict[str, PostingList]) -> Iterator[DocId]:
        cursors: List[Cursor] = []
        for term in self.terms:
            iterator = term.execute(posting_lists)
            cursors.append(Cursor(iterator))

        current_doc = -1
        seen_count = 0
        while True:
            cursor = heapq.heappop(cursors)
            try:
                cursor = cursor.next_from(current_doc)
                next_doc = cursor.head
                if next_doc == current_doc:
                    seen_count += 1
                else:
                    current_doc = next_doc
                    seen_count = 1
                if seen_count == len(self.terms):
                    yield current_doc
                heapq.heappush(cursors, cursor)
            except StopIteration:
                break


class Disjunction(Query):
    # Example: "apple or pear"
    terms: List[Query]

    def __init__(self, terms: List[Query]):
        self.terms = terms

    def __str__(self):
        result = []
        for term in self.terms:
            if len(result) != 0:
                result.append("or")
            result.append(str(term))
        return f'({" ".join(result)})'

    def execute(self, posting_lists: Dict[str, PostingList]) -> Iterator[DocId]:
        buckets: List[Cursor] = []
        for term in self.terms:
            iterator = term.execute(posting_lists)
            buckets.append(Cursor(iterator))

        current_doc = -1
        while buckets:
            cursor = heapq.heappop(buckets)
            try:
                next_doc = cursor.head
                if next_doc != current_doc:
                    current_doc = next_doc
                    yield current_doc
                heapq.heappush(buckets, cursor.__next__())
            except StopIteration:
                pass


class Negation(Query):
    # Example: "not apple"
    # "not (apple and kiwi)"
    term: Query

    def __init__(self, term: Query):
        self.term = term

    def __str__(self):
        return f'(not {self.term})'

    def execute(self, posting_lists: Dict[str, PostingList]) -> Iterator[DocId]:
        bad_docs = self.term.execute(posting_lists)
        all_docs = Literal("*").execute(posting_lists)
        for next_bad_doc in bad_docs:
            while True:
                next_doc = all_docs.__next__()
                if next_doc == next_bad_doc:
                    break
                yield next_doc
        for next_doc in all_docs:
            yield next_doc
