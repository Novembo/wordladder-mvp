"""Word Ladder graph construction using intermediate bucket hashing."""
from __future__ import annotations

from collections import defaultdict


def differs_by_one_letter(a: str, b: str) -> bool:
    """Return True if words a and b have the same length and differ by exactly one letter."""
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1


def build_graph(words: set[str] | list[str]) -> dict[str, set[str]]:
    """Construct an adjacency graph where edges connect words differing by 1 character.

    Complexity is O(N * L) using wildcard bucket grouping (e.g. c_ld, co_d, col_).
    """
    clean_words = {w.strip().lower() for w in words if w and w.strip()}
    buckets: dict[str, list[str]] = defaultdict(list)

    for word in clean_words:
        for i in range(len(word)):
            pattern = word[:i] + "_" + word[i + 1:]
            buckets[pattern].append(word)

    graph: dict[str, set[str]] = {w: set() for w in clean_words}
    for group in buckets.values():
        if len(group) > 1:
            for w in group:
                graph[w].update(x for x in group if x != w)

    return graph

