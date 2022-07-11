"""
Type definitions related to posting lists
"""

from typing import List

# Each document is assigned a unique sequential integer ID.
DocId = int

# A posting list for contains the IDs of all documents matching a given term.
# The document IDs are sorted in ascending order to allow for fast union/intersection.
PostingList = List[DocId]
