import random
import pytest

from app.core import GameError, Match, Pack, differs_by_one_letter, normalize
from app.graph import build_graph
from app.services.dictionary import strip_accents

WORDS = [
    "cold", "cord", "card", "ward", "warm", "worm", "word", "wood", "wool",
    "fool", "food", "foot", "fort", "form", "farm", "firm", "fire", "five",
    "live", "line", "lone", "bone", "bane", "bank", "bark", "dark", "dart",
    "part", "past", "post", "host", "most", "cost", "cast", "case", "cave",
    "gave", "gate", "hate", "date", "data", "head", "lead", "load", "boat",
    "coat", "chat", "that", "what", "wait", "bait", "ball", "fall", "tall",
    "tell", "hell", "bell", "belt", "best", "rest", "rust", "dust", "dusk",
    "cat", "bat", "rat", "hat", "hot", "pot", "dot", "dog", "log", "leg"
]


def make_pack():
    g = build_graph(WORDS)
    playable = {w for w, nb in g.items() if nb}
    return Pack("en", {w: g[w] for w in playable}, {})


def test_strip_accents_and_normalize():
    assert strip_accents("Héllò") == "hello"
    assert normalize("  ÉtÉ ") == "ete"


def test_differs_by_one_letter():
    assert differs_by_one_letter("cold", "cord")
    assert not differs_by_one_letter("cold", "warm")
    assert not differs_by_one_letter("cold", "colder")


def force_start(m, word):
    m.used = {word}
    m.current = word
    m.word_length = len(word)
    m.to_move = 0


def test_constant_word_length_rule():
    m = Match(make_pack(), "basic", "duo", rng=random.Random(10))
    force_start(m, "cold")
    assert m.word_length == 4

    # Attempting to play a word of length 3 should raise wrong_length
    with pytest.raises(GameError) as exc:
        m.play(0, "cat")
    assert exc.value.code == "wrong_length"


def test_duo_flow_and_rules():
    m = Match(make_pack(), "basic", "duo", rng=random.Random(1))
    force_start(m, "cold")
    m.play(0, "cord")

    # Not player 0's turn
    with pytest.raises(GameError) as exc:
        m.play(0, "card")
    assert exc.value.code == "not_your_turn"

    # Already used word
    with pytest.raises(GameError) as exc:
        m.play(1, "cold")
    assert exc.value.code == "already_used"

    # Unknown word
    with pytest.raises(GameError) as exc:
        m.play(1, "zzzz")
    assert exc.value.code == "unknown_word"

    # Too many letter differences
    with pytest.raises(GameError) as exc:
        m.play(1, "warm")
    assert exc.value.code == "not_one_letter"

    m.play(1, "card")
    assert m.current == "card"
    assert m.to_move == 0


def test_three_lives_system_and_timeout():
    m = Match(make_pack(), "basic", "duo", rng=random.Random(2))
    force_start(m, "cold")
    m.play(0, "cord")
    assert m.lives == [3, 3]

    # 1st timeout for Player 1: loses 1 life, game continues in part 1
    m.timeout(1)
    assert m.lives == [3, 2]
    assert m.part == 1
    assert m.scores == [0, 0]

    # 2nd timeout for Player 1: loses 2nd life
    m.timeout(1)
    assert m.lives == [3, 1]
    assert m.part == 1

    # 3rd timeout for Player 1: loses last life -> part ends, Player 0 gets the point
    m.timeout(1)
    assert m.scores == [1, 0]
    assert m.part == 2
    # Lives reset to 3 for the new round
    assert m.lives == [3, 3]


def test_solo_computer_turn():
    m = Match(make_pack(), "advanced", "solo", rng=random.Random(3))
    assert m.time_limit == 40  # 20 + 20s
    if not m.finished and m.to_move == 0:
        options = sorted(m.available_from(m.current))
        if options:
            m.play(0, options[0])
            assert m.finished or m.to_move == 0 or m.part > 1
