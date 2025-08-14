from __future__ import annotations

import questionary
from random import choice
from typing import Optional

from ..core.engine import is_game_over, play_round
from ..core.types import Hand, Player, RoundResult, Rules


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


def pick_hand_menu(player_name: str) -> Optional[Hand]:
    sel = questionary.select(
        f"{player_name} の手を選んでください",
        choices=[
            questionary.Choice("グー (g)", Hand.ROCK),
            questionary.Choice("チョキ (c)", Hand.SCISSORS),
            questionary.Choice("パー (p)", Hand.PAPER),
            questionary.Choice("— ステータスを表示 —", "status"),
            questionary.Choice("— ルールを表示 —", "rules"),
            questionary.Choice("— 終了 —", "quit"),
        ],
    ).ask()
    if sel is None:
        return None
    if sel == "quit":
        return None
    if sel == "status":
        return "status"  # type: ignore[return-value]
    if sel == "rules":
        return "rules"  # type: ignore[return-value]
    return sel  # Hand


def interactive_loop(p1: Player, p2: Player, rules: Rules, mode: str, input_mode: str) -> int:
    print("\nコマンド: :help / :status / :rules / :quit")
    while True:
        p1_hand: Optional[Hand] = None
        p2_hand: Optional[Hand] = None

        # P1 input
        while p1_hand is None:
            if input_mode == "menu":
                sel = pick_hand_menu(p1.name)
                if sel is None:
                    print("Bye!")
                    return 0
                if sel == "status":  # type: ignore[comparison-overlap]
                    print_status(p1, p2, rules)
                    continue
                if sel == "rules":  # type: ignore[comparison-overlap]
                    print_rules(rules)
                    continue
                p1_hand = sel  # type: ignore[assignment]
            else:
                h = prompt_hand(p1.name)
                if h is not None:
                    p1_hand = h
                    break
                # command handling (direct mode)
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
                if input_mode == "menu":
                    sel2 = pick_hand_menu(p2.name)
                    if sel2 is None:
                        print("Bye!")
                        return 0
                    if sel2 == "status":  # type: ignore[comparison-overlap]
                        print_status(p1, p2, rules)
                        continue
                    if sel2 == "rules":  # type: ignore[comparison-overlap]
                        print_rules(rules)
                        continue
                    p2_hand = sel2  # type: ignore[assignment]
                else:
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

