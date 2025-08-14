from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from random import choice
from typing import Optional

from ..core.data import PHYSIQUE_CAPACITY
from ..core.types import Rules, Player
from .wizard import run_setup_wizard
from .title import title_screen
from .console import console
from .loop import interactive_loop, print_rules, print_status


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="calorie-clash",
        description=(
            "ポイントを稼ぐか、満腹で脱落か──胃袋の限界バトル。\n"
            "Hungry Janken (Calorie Clash) — Python CLI"
        ),
    )
    parser.add_argument("--mode", choices=["1p", "2p"], default="1p", help="1p (vs CPU) or 2p")
    parser.add_argument("--input", choices=["direct", "menu"], default="direct", help="Input mode: direct or menu (questionary)")
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
    parser.add_argument("--wizard", action="store_true", help="Launch interactive setup wizard (questionary)")
    parser.add_argument("--anim", choices=["on", "off"], default="on", help="Enable/disable janken animation")
    parser.add_argument("--anim-speed", type=float, default=1.0, help="Seconds between ジャン→ケン→ポン (default 1.0)")
    return parser.parse_args(argv)


def prompt_hand(player_name: str) -> Optional[Hand]:
    raw = input(f"{player_name} の手を入力 [g/c/p]（g=グー, c=チョキ, p=パー）: ").strip()
    if raw.startswith(":"):
        return None
    return Hand.from_input(raw)




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


def main(argv: Optional[list[str]] = None) -> int:
    raw_argv = sys.argv[1:] if argv is None else argv
    ns = parse_args(raw_argv)
    # If no arguments given, show title screen by default
    if len(raw_argv) == 0:
        start, ns = title_screen(ns)
        if not start:
            return 0
    if ns.wizard:
        ns = run_setup_wizard(ns)
    rules = Rules(target_points=ns.target, tie_rule_both_eat=(ns.tie == "bothEat"))

    if ns.mode == "1p":
        cap = PHYSIQUE_CAPACITY[ns.physique]
        p1 = Player(name=ns.p1_name, max_kcal=cap)
        p2 = Player(name=ns.p2_name, max_kcal=cap)
    else:
        # For 2P, use wizard-provided physiques if available; otherwise prompt
        if hasattr(ns, "_p1_physique") and hasattr(ns, "_p2_physique"):
            p1 = Player(name=ns.p1_name, max_kcal=PHYSIQUE_CAPACITY[getattr(ns, "_p1_physique")])
            p2 = Player(name=ns.p2_name, max_kcal=PHYSIQUE_CAPACITY[getattr(ns, "_p2_physique")])
        else:
            print("2P モード: 体格（small/medium/large）を P1/P2 で選んでください。")
            def pick_cap(label: str) -> int:
                while True:
                    raw = input(f"{label} physique [small/medium/large] (default: medium): ").strip().lower() or "medium"
                    if raw in PHYSIQUE_CAPACITY:
                        return PHYSIQUE_CAPACITY[raw]
                    print("無効な入力です。 small/medium/large を入力してください。")

            p1 = Player(name=ns.p1_name, max_kcal=pick_cap("P1"))
            p2 = Player(name=ns.p2_name, max_kcal=pick_cap("P2"))

    console.print("\n[title]=== Calorie Clash (Python CLI) ===[/title]")
    console.print("[info]ポイントを稼ぐか、満腹で脱落か──胃袋の限界バトル。[/]\n")
    print_rules(rules)
    print_status(p1, p2, rules)

    anim_enabled = (ns.anim == "on")
    anim_interval = max(0.0, float(ns.anim_speed))
    language = getattr(ns, "language", "ja")
    return interactive_loop(p1, p2, rules, ns.mode, ns.input, anim_enabled, anim_interval, language)


if __name__ == "__main__":
    raise SystemExit(main())
