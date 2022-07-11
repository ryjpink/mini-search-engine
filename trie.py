from typing import List


class TrieNode:
    def __init__(self, end=False):
        self.end = end
        self.trie_dict = {}


class Trie:
    def __init__(self):
        self.root_node = TrieNode()

    def add(self, word: str):
        check_node = self.root_node
        for i, c in enumerate(word):
            if not c in check_node.trie_dict:
                if i == len(word) - 1:
                    new_node = TrieNode(True)
                else:
                    new_node = TrieNode()
                check_node.trie_dict[c] = new_node
                check_node = new_node
            else:
                if i == len(word) - 1:
                    check_node.trie_dict[c].end = True
                else:
                    check_node = check_node.trie_dict[c]


    def complete(self, prefix: str) -> List[str]:
        check_node = self.root_node
        answer = []
        self.path = []
        for c in prefix:
            if c not in check_node.trie_dict:
                return answer
            else:
                self.path.append(c)
                check_node = check_node.trie_dict[c]

        def backtrack(cur_node):
            if cur_node.end is True:
                answer.append("".join(self.path))
            for candidate in cur_node.trie_dict:
                self.path.append(candidate)
                backtrack(cur_node.trie_dict[candidate])
                self.path.pop()

        backtrack(check_node)
        return answer


if __name__ == "__main__":
    trie = Trie()
    words = ["cherry", "chocolate", "cocoa", "chorizo", "coffee", "cheddar", "cheese", "chowder", "pineapple"]
    for word in words:
        trie.add(word)
    prefix = input("query> ")
    print(trie.complete(prefix))
