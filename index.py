from typing import Dict, List
from collections import defaultdict
from posting_list import PostingList, DocId
from document import Document
from query import Query


class SearchIndex:
    documents: Dict[DocId, Document]
    posting_lists: Dict[str, PostingList]

    def __init__(self, documents: List[Document]):
        self.doc_id = 0
        self.documents = {}
        self.posting_lists = defaultdict(list)
        for item in documents:
            self.add(item)

    def add(self, doc: Document):
        self.documents[self.doc_id] = doc
        contain_words = doc.words()
        contain_words.add('*')
        for word in contain_words:
            self.posting_lists[word].append(self.doc_id)
        self.doc_id += 1

    def search(self, query: Query) -> List[Document]:
        doc_ids = query.execute(self.posting_lists)
        docs = [self.documents[doc_id] for doc_id in doc_ids]
        return docs