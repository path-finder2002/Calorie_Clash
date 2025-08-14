from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from random import choice
from typing import Optional

from ..core.game import (
    Hand,
    PHYSIQUE_CAPACITY,
    Player,
    RoundResult,
    Rules,
    is_game_over,
    play_round,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="calorie-clash",
        description=(
            "ポイントを稼ぐか、満腹で脱落か──胃袋の限界バトル。\n"
            "Hungry Janken (Calorie Clash) — Python CLI"
        ),
    )
    parser.add_argument("--mode", choices=["1p", "2p"], default="1p", help="1p (vs CPU) or 2p")
    parser.add_argument("--target", type=int, default=50, help="Target points to win (default 50)")
    parser.add_argument(
        "--physique",
        choices=list(PHYSIQUE_CAPACITY.keys()),
        default="medium",
        help="Capacity preset for both players in 1p; for 2p you can customize in the prompts",
    )
    parser.add_argument("--p1-name", default="P1", help="Player 1 name")
    parser.add_argument("--p2-name", default="CPU", help="Player 2 name")
    parser.add_argument("--tie", choices=["rematch", "bothEat"], default="rematch", help="Tie rule")
    return parser.parse_args(argv)


def prompt_hand(player_name: str) -> Optional[Hand]:
    raw = input(f"{player_name} の手を入力 [g/c/p]（g=グー, c=チョキ, p=パー）: ").strip()
    if raw.startswith(":"):
        return None
    return Hand.from_input(raw)


def cpu_pick() -> Hand:
    return choice([Hand.ROCK, Hand.SCISSORS, Hand.PAPER])


def print_status(p1: Player, p2: Player, rules: Rules) -> None:
    print(
        f"\nStatus: {p1.name}: {p1.points}pt / {p1.consumed_kcal}/{p1.max_kcal}kcal | "
        f"{p2.name}: {p2.points}pt / {p2.consumed_kcal}/{p2.max_kcal}kcal | target={rules.target_points}\n"
    )


def print_rules(rules: Rules) -> None:
    print("\nRules:")
    print(f"- target points: {rules.target_points}")
    print(f"- tie: {'both eat own food' if rules.tie_rule_both_eat else 'rematch'}\n")


def interactive_loop(p1: Player, p2: Player, rules: Rules, mode: str) -> int:
    print("\nコマンド: :help / :status / :rules / :quit")
    while True:
        p1_hand: Optional[Hand] = None
        p2_hand: Optional[Hand] = None

        # P1 input
        while p1_hand is None:
            h = prompt_hand(p1.name)
            if h is not None:
                p1_hand = h
                break
            # command handling
            cmd = input("") if False else ""  # dummy to keep structure
            last = ""
            # Re-read the last raw since prompt_hand consumed it; we can't here, so reprompt for command.
            raw = input(":command> ").strip().lower()
            if raw in {":quit", ":q", ":exit"}:
                print("Bye!")
                return 0
            if raw in {":status", ":s"}:
                print_status(p1, p2, rules)
                continue
            if raw in {":rules", ":r"}:
                print_rules(rules)
                continue
            if raw in {":help", ":h"}:
                print(
                    "\n:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。\n"
                )
                continue
            # Otherwise, treat original input as invalid
            print("無効な入力です。 g/c/p または :help を入力してください。")

        # P2 input / CPU
        if mode == "1p":
            p2_hand = cpu_pick()
            print(f"{p2.name} は手を選びました。")
        else:
            while p2_hand is None:
                p2_hand = prompt_hand(p2.name)
                if p2_hand is None:
                    raw = input(":command> ").strip().lower()
                    if raw in {":quit", ":q", ":exit"}:
                        print("Bye!")
                        return 0
                    if raw in {":status", ":s"}:
                        print_status(p1, p2, rules)
                        p2_hand = None
                        continue
                    if raw in {":rules", ":r"}:
                        print_rules(rules)
                        p2_hand = None
                        continue
                    if raw in {":help", ":h"}:
                        print(
                            "\n:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。\n"
                        )
                        p2_hand = None
                        continue
                    print("無効な入力です。 g/c/p または :help を入力してください。")

        # Reveal hands
        def show(h: Hand) -> str:
            return {Hand.ROCK: "グー", Hand.SCISSORS: "チョキ", Hand.PAPER: "パー"}[h]

        print(f"\n{p1.name}: {show(p1_hand)} vs {p2.name}: {show(p2_hand)}")
        result: RoundResult = play_round(p1, p2, p1_hand, p2_hand, rules)
        if result.tie:
            print("→ あいこ！")
        else:
            assert result.winner and result.winner_food
            print(
                f"→ 勝者: {result.winner.name} (+{result.winner_gained_points}pt) "
                f"/ 敗者は『{result.winner_food.name}』を食べて +{result.loser_added_kcal}kcal"
            )
        print_status(p1, p2, rules)

        over, champion = is_game_over(p1, p2, rules)
        if over:
            print(f"🏆 勝者: {champion.name}! お疲れさまでした。\n")
            return 0


def main(argv: Optional[list[str]] = None) -> int:
    ns = parse_args(argv or sys.argv[1:])
    rules = Rules(target_points=ns.target, tie_rule_both_eat=(ns.tie == "bothEat"))

    if ns.mode == "1p":
        cap = PHYSIQUE_CAPACITY[ns.physique]
        p1 = Player(name=ns.p1_name, max_kcal=cap)
        p2 = Player(name=ns.p2_name, max_kcal=cap)
    else:
        # For 2P, prompt physiques
        print("2P モード: 体格（small/medium/large）を P1/P2 で選んでください。")
        def pick_cap(label: str) -> int:
            while True:
                raw = input(f"{label} physique [small/medium/large] (default: medium): ").strip().lower() or "medium"
                if raw in PHYSIQUE_CAPACITY:
                    return PHYSIQUE_CAPACITY[raw]
                print("無効な入力です。 small/medium/large を入力してください。")

        p1 = Player(name=ns.p1_name, max_kcal=pick_cap("P1"))
        p2 = Player(name=ns.p2_name, max_kcal=pick_cap("P2"))

    print("\n=== Calorie Clash (Python CLI) ===")
    print("ポイントを稼ぐか、満腹で脱落か──胃袋の限界バトル。\n")
    print_rules(rules)
    print_status(p1, p2, rules)

    return interactive_loop(p1, p2, rules, ns.mode)


if __name__ == "__main__":
    raise SystemExit(main())

