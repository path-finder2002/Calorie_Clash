from __future__ import annotations

from random import choice
from typing import Dict, List, Optional, Tuple

from .data import DEFAULT_FOODS
from .types import Food, Hand, Player, RoundResult, Rules


def beats(a: Hand, b: Hand) -> bool:
    return (
        (a == Hand.ROCK and b == Hand.SCISSORS)
        or (a == Hand.SCISSORS and b == Hand.PAPER)
        or (a == Hand.PAPER and b == Hand.ROCK)
    )


def pick_food_for(hand: Hand, foods: Dict[Hand, List[Food]] = DEFAULT_FOODS) -> Food:
    return choice(foods[hand])


def play_round(
    p1: Player,
    p2: Player,
    p1_hand: Hand,
    p2_hand: Hand,
    rules: Rules,
    foods: Dict[Hand, List[Food]] = DEFAULT_FOODS,
) -> RoundResult:
    if p1_hand == p2_hand:
        if rules.tie_rule_both_eat:
            f1 = pick_food_for(p1_hand, foods)
            f2 = pick_food_for(p2_hand, foods)
            p1.consumed_kcal += f1.kcal
            p2.consumed_kcal += f2.kcal
        return RoundResult(
            winner=None,
            loser=None,
            tie=True,
            winner_food=None,
            loser_added_kcal=0,
            winner_gained_points=0,
        )

    p1_wins = beats(p1_hand, p2_hand)
    if p1_wins:
        win_player, lose_player, win_hand = p1, p2, p1_hand
    else:
        win_player, lose_player, win_hand = p2, p1, p2_hand

    win_food = pick_food_for(win_hand, foods)
    gained_points = win_food.points
    win_player.points += gained_points
    lose_player.consumed_kcal += win_food.kcal

    return RoundResult(
        winner=win_player,
        loser=lose_player,
        tie=False,
        winner_food=win_food,
        loser_added_kcal=win_food.kcal,
        winner_gained_points=gained_points,
    )


def is_game_over(p1: Player, p2: Player, rules: Rules) -> Tuple[bool, Optional[Player]]:
    # Points victory
    if p1.points >= rules.target_points and p2.points >= rules.target_points:
        # Simultaneous reach: higher points wins; tie by points falls back to lower kcal consumed
        if p1.points == p2.points:
            return True, (p1 if p1.consumed_kcal < p2.consumed_kcal else p2)
        return True, (p1 if p1.points > p2.points else p2)
    if p1.points >= rules.target_points:
        return True, p1
    if p2.points >= rules.target_points:
        return True, p2

    # Fullness bust
    if p1.is_busted and p2.is_busted:
        # If both bust, lower consumed wins (ate less)
        return True, (p1 if p1.consumed_kcal < p2.consumed_kcal else p2)
    if p1.is_busted:
        return True, p2
    if p2.is_busted:
        return True, p1

    return False, None

