"""Prefix tree to help with searching for drug name matches."""

from typing import Dict, Optional


class Node:
    def __init__(self) -> None:
        self.children: Dict[str, "Node"] = {}
        self.leaf = False
        self.drug_id: str | None = None  # ID is stored at end of word/leaf


class PrefixTree:
    def __init__(self) -> None:
        self.root = Node()

    def insert(self, word: str, drug_id: str) -> None:
        """Insert word into the tree."""
        node = self.root
        for char in word:
            node = node.children.setdefault(char, Node())

        node.leaf = True
        node.drug_id = drug_id

    def find_starts_with(self, target: str) -> Optional[str]:
        """Check if any string in the list starts with this target prefix."""
        node = self.root
        for char in target:
            if char not in node.children:
                return None
            node = node.children[char]

        # prefix matches - find first full word
        return self._find_first_full_word_below(node)

    def _find_first_full_word_below(self, node: Node) -> Optional[str]:
        """DFS to find first full word that falls below the given node."""
        if node.leaf:
            return node.drug_id
        for child in node.children.values():
            result = self._find_first_full_word_below(child)
            if result:
                return result

        return None

    def find_longest_prefix(self, target: str) -> Optional[str]:
        """Find longest match where target string starts with the string in the
        list."""
        longest = None
        node = self.root
        for char in target:
            if node.leaf:
                longest = node.drug_id
            if char not in node.children:
                break
            node = node.children[char]

        if node.leaf:
            return node.drug_id

        return longest

    def get_closest_match(self, target: str) -> Optional[str]:
        """Get closest match of target string by checking if it is close enough
        to any string in this tree."""
        startswith = self.find_starts_with(target)

        if startswith is None:
            return self.find_longest_prefix(target)

        return startswith
