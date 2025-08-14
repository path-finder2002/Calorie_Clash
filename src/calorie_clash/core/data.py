from __future__ import annotations

from typing import Dict, List

from .types import Food, Hand


DEFAULT_FOODS: Dict[Hand, List[Food]] = {
    Hand.ROCK: [
        Food("グラタン", 18),
        Food("グミ", 8),
        Food("グリルチキン", 22),
    ],
    Hand.SCISSORS: [
        Food("チョコ", 12),
        Food("チキン", 16),
        Food("チャーハン", 24),
    ],
    Hand.PAPER: [
        Food("パスタ", 20),
        Food("パンケーキ", 26),
        Food("パエリア", 28),
    ],
}

PHYSIQUE_CAPACITY = {
    "small": 800,
    "medium": 1000,
    "large": 1300,
}
