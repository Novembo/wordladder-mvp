"""Core Word Ladder game logic — framework-independent, deterministic, highly testable."""
from __future__ import annotations

import random
import time
import uuid
from dataclasses import dataclass, field

from .graph import build_graph, differs_by_one_letter
from .services.dictionary import strip_accents

# Level durations increased by +20s for optimal educational pacing
TIME_LIMITS = {"basic": 80, "intermediate": 60, "advanced": 40}
LEVELS = tuple(TIME_LIMITS)
MIN_START_NEIGHBORS = 3
GRACE_SECONDS = 1.0
MAX_LIVES = 3


class GameError(Exception):
    """Domain rule violation; rejects the move without modifying game state."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def normalize(word: str) -> str:
    return strip_accents(word.strip().lower())


@dataclass
class Pack:
    """Language pack containing word adjacency graph and difficulty pools."""

    lang: str
    graph: dict[str, set[str]]
    level_words: dict[str, set[str]]
    version: str = "1.0.0"

    def pool(self, level: str) -> set[str]:
        return self.level_words.get(level) or set(self.graph)


@dataclass
class Match:
    pack: Pack
    level: str
    mode: str  # "solo" (vs computer) or "duo" (pass & play or 2-player)
    play_all_parts: bool = False
    rng: random.Random = field(default_factory=random.Random)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    scores: list[int] = field(default_factory=lambda: [0, 0])
    lives: list[int] = field(default_factory=lambda: [MAX_LIVES, MAX_LIVES])
    part: int = 1
    used: set[str] = field(default_factory=set)
    current: str = ""
    word_length: int = 0  # Strict constant word length for the entire match
    to_move: int = 0
    turn_started: float = 0.0
    finished: bool = False
    winner: int | None = None
    last_event: str = ""

    def __post_init__(self):
        if self.level not in TIME_LIMITS:
            raise GameError("bad_level", f"Unknown level: {self.level}")
        if self.mode not in ("solo", "duo"):
            raise GameError("bad_mode", f"Unknown mode: {self.mode}")
        self._start_part()

    @property
    def time_limit(self) -> int:
        return TIME_LIMITS[self.level]

    def available_from(self, word: str) -> set[str]:
        return self.pack.graph.get(word, set()) - self.used

    def state(self) -> dict:
        return {
            "match_id": self.id,
            "part": self.part,
            "scores": list(self.scores),
            "lives": list(self.lives),
            "word_length": self.word_length,
            "current_word": self.current,
            "to_move": self.to_move,
            "time_limit": self.time_limit,
            "used_count": len(self.used),
            "finished": self.finished,
            "winner": self.winner,
            "event": self.last_event,
        }

    def _start_part(self):
        # 1. If match just started, pick initial word to lock word_length N
        if self.word_length == 0:
            pool = [
                w for w in self.pack.pool(self.level)
                if w not in self.used and len(self.available_from(w)) >= MIN_START_NEIGHBORS
            ]
            if not pool:
                pool = [w for w in self.pack.graph if w not in self.used and self.available_from(w)]
            if not pool:
                raise GameError("no_start_word", "No start word available.")
            chosen = self.rng.choice(sorted(pool))
            self.word_length = len(chosen)
            self.current = chosen
        else:
            # 2. Subsequent rounds strictly filter for the same length N
            pool = [
                w for w in self.pack.pool(self.level)
                if len(w) == self.word_length and w not in self.used and len(self.available_from(w)) >= MIN_START_NEIGHBORS
            ]
            if not pool:
                pool = [
                    w for w in self.pack.graph
                    if len(w) == self.word_length and w not in self.used and self.available_from(w)
                ]
            if not pool:
                raise GameError("no_start_word", f"No start word of length {self.word_length} available.")
            self.current = self.rng.choice(sorted(pool))

        self.used.add(self.current)
        self.to_move = (self.part - 1) % 2
        self.turn_started = time.monotonic()
        self._run_computer()

    def _end_part(self, loser: int, reason: str):
        winner = 1 - loser
        self.scores[winner] += 1
        self.last_event = f"part_{self.part}_{reason}_loser_{loser}"
        done = self.scores[winner] == 2 and not self.play_all_parts
        if self.part == 3 or done:
            self.finished = True
            self.winner = 0 if self.scores[0] > self.scores[1] else 1
            return
        self.part += 1
        # Refresh lives for each new round
        self.lives = [MAX_LIVES, MAX_LIVES]
        try:
            self._start_part()
        except GameError:
            self.finished = True
            self.winner = None if self.scores[0] == self.scores[1] else (
                0 if self.scores[0] > self.scores[1] else 1)
            self.last_event = "no_start_word_left"

    def play(self, player: int, word: str) -> dict:
        self._check_turn(player)
        if self._expired():
            return self._handle_timeout(player)

        w = normalize(word)
        # Strict word length check
        if len(w) != self.word_length:
            raise GameError("wrong_length", f"Le mot doit comporter exactement {self.word_length} lettres.")
        if w not in self.pack.graph:
            raise GameError("unknown_word", f"« {w} » n'est pas dans le dictionnaire.")
        if w in self.used:
            raise GameError("already_used", f"« {w} » a déjà été utilisé.")
        if not differs_by_one_letter(self.current, w):
            raise GameError("not_one_letter", "Il faut changer exactement une lettre.")

        self._accept(w)
        return self.state()

    def timeout(self, player: int) -> dict:
        self._check_turn(player)
        return self._handle_timeout(player)

    def _handle_timeout(self, player: int) -> dict:
        if self.lives[player] > 1:
            self.lives[player] -= 1
            self.turn_started = time.monotonic()
            self.last_event = f"life_lost_player_{player}"
            return self.state()
        else:
            self.lives[player] = 0
            self._end_part(player, "timeout")
            return self.state()

    def _accept(self, word: str):
        self.used.add(word)
        self.current = word
        self.to_move = 1 - self.to_move
        self.turn_started = time.monotonic()
        self.last_event = "move_ok"
        if not self.available_from(word):
            # Opponent is trapped at a dead end
            self._end_part(self.to_move, "dead_end")
            return
        self._run_computer()

    def _check_turn(self, player: int):
        if self.finished:
            raise GameError("match_finished", "Match is finished.")
        if player != self.to_move:
            raise GameError("not_your_turn", "Ce n'est pas votre tour.")

    def _expired(self) -> bool:
        return time.monotonic() - self.turn_started > self.time_limit + GRACE_SECONDS

    def _run_computer(self):
        if self.mode != "solo" or self.finished or self.to_move != 1:
            return
        word = self.pick_computer_word()
        if word is None:
            self._end_part(1, "dead_end")
            return
        self._accept(word)

    def pick_computer_word(self) -> str | None:
        options = self.available_from(self.current)
        if not options:
            return None
        in_level = options & self.pack.pool(self.level)
        options = in_level or options
        smart_chance = {"basic": 0.0, "intermediate": 0.5, "advanced": 1.0}[self.level]
        if self.rng.random() < smart_chance:
            best = min(len(self.available_from(w) - {w}) for w in options)
            options = {w for w in options if len(self.available_from(w) - {w}) == best}
        return self.rng.choice(sorted(options))
