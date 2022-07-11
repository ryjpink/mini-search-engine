from typing import List


class TrieNode:
    def __init__(self, end=False):
        self.end = end
        self.trie_dict = {}


class Trie:
    def __init__(self):
        self.root_node = TrieNode()

    def add(self, word: str):
        cur_node = self.root_node
        for c in word:
            if c not in cur_node.trie_dict:
                cur_node.trie_dict[c] = TrieNode()
            cur_node = cur_node.trie_dict[c]
        cur_node.end = True

    def complete(self, prefix: str) -> List[str]:
        cur_node = self.root_node
        answer = []
        path = []
        for c in prefix:
            if c not in cur_node.trie_dict:
                return answer
            else:
                path.append(c)
                cur_node = cur_node.trie_dict[c]

        def backtrack(cur_node):
            if cur_node.end is True:
                answer.append("".join(path))
            for candidate in cur_node.trie_dict:
                path.append(candidate)
                backtrack(cur_node.trie_dict[candidate])
                path.pop()

        backtrack(cur_node)
        return answer


if __name__ == "__main__":
    trie = Trie()
    words = ["cherry", "chocolate", "cocoa", "chorizo", "coffee", "cheddar", "cheese", "chowder", "pineapple"]
    for word in words:
        trie.add(word)
    prefix = input("query> ")
    print(trie.complete(prefix))
