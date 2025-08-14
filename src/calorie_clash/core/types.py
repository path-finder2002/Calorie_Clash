from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Hand(Enum):
    ROCK = auto()
    SCISSORS = auto()
    PAPER = auto()

    @staticmethod
    def from_input(token: str) -> Optional["Hand"]:
        t = token.strip().lower()
        if t in {"g", "r", "rock", "gu", "ぐー", "グー"}:
            return Hand.ROCK
        if t in {"c", "s", "scissors", "cho", "ちょき", "チョキ"}:
            return Hand.SCISSORS
        if t in {"p", "paper", "pa", "ぱー", "パー"}:
            return Hand.PAPER
        return None


@dataclass(frozen=True)
class Food:
    name: str
    kcal: int

    @property
    def points(self) -> int:
        # Simple scoring: length of the name (non-space) times 2
        return max(1, len(self.name.replace(" ", ""))) * 2


@dataclass
class Player:
    name: str
    max_kcal: int = 100
    points: int = 0
    consumed_kcal: int = 0

    @property
    def is_busted(self) -> bool:
        return self.consumed_kcal >= self.max_kcal


@dataclass
class Rules:
    target_points: int = 50
    tie_rule_both_eat: bool = False  # if True, both eat their own food on tie


@dataclass
class RoundResult:
    winner: Optional[Player]
    loser: Optional[Player]
    tie: bool
    winner_food: Optional[Food]
    loser_added_kcal: int
    winner_gained_points: int

