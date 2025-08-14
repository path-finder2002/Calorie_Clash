from __future__ import annotations

from typing import Dict, List, Optional
import csv
import os

from .types import Food, Hand


DEFAULT_FOODS: Dict[Hand, List[Food]] = {
    Hand.ROCK: [
        Food("グラタン", 180),
        Food("グミ", 80),
        Food("グリルチキン", 220),
    ],
    Hand.SCISSORS: [
        Food("チョコ", 120),
        Food("チキン", 160),
        Food("チャーハン", 240),
    ],
    Hand.PAPER: [
        Food("パスタ", 200),
        Food("パンケーキ", 260),
        Food("パエリア", 280),
    ],
}

PHYSIQUE_CAPACITY = {
    "small": 800,
    "medium": 1000,
    "large": 1300,
}


HAND_ALIASES = {
    "g": Hand.ROCK,
    "gu": Hand.ROCK,
    "rock": Hand.ROCK,
    "ぐー": Hand.ROCK,
    "グー": Hand.ROCK,
    "c": Hand.SCISSORS,
    "s": Hand.SCISSORS,
    "cho": Hand.SCISSORS,
    "scissors": Hand.SCISSORS,
    "ちょき": Hand.SCISSORS,
    "チョキ": Hand.SCISSORS,
    "p": Hand.PAPER,
    "pa": Hand.PAPER,
    "paper": Hand.PAPER,
    "ぱー": Hand.PAPER,
    "パー": Hand.PAPER,
}


def parse_hand_token(token: str) -> Optional[Hand]:
    key = (token or "").strip().lower()
    return HAND_ALIASES.get(key)


def load_foods_csv(path: str, *, extend_from_defaults: bool = True) -> Dict[Hand, List[Food]]:
    """Load foods from a CSV file with columns: hand,name,kcal.

    - hand: one of g/rock/ぐー/c/scissors/チョキ/p/paper/パー ... (aliases supported)
    - name: food name (string)
    - kcal: integer kcal amount

    Returns a dict {Hand: List[Food]}. If `extend_from_defaults` is True (default),
    the resulting lists start with DEFAULT_FOODS[hand] and then add loaded foods.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    result: Dict[Hand, List[Food]] = {h: (list(DEFAULT_FOODS[h]) if extend_from_defaults else []) for h in Hand}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Normalize headers to lower
        headers = [h.strip().lower() for h in (reader.fieldnames or [])]
        required = {"hand", "name", "kcal"}
        if not required.issubset(set(headers)):
            raise ValueError("CSV must include columns: hand,name,kcal")
        has_points = "points" in set(headers)
        for row in reader:
            hand = parse_hand_token(row.get("hand", ""))
            name = (row.get("name", "") or "").strip()
            kcal_s = (row.get("kcal", "") or "").strip()
            if not hand or not name or not kcal_s:
                continue
            try:
                kcal = int(float(kcal_s))
            except Exception:
                continue
            custom_pts = None
            if has_points:
                pts_s = (row.get("points", "") or "").strip()
                if pts_s:
                    try:
                        custom_pts = int(float(pts_s))
                    except Exception:
                        custom_pts = None
            result[hand].append(Food(name=name, kcal=kcal, custom_points=custom_pts))
    return result
