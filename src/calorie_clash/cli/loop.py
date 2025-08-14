from __future__ import annotations

import questionary
from random import choice
from time import sleep
from typing import Optional

from ..core.engine import is_game_over, play_round
from ..core.types import Hand, Player, RoundResult, Rules
from .console import console


def prompt_hand(player_name: str) -> Optional[Hand]:
    raw = input(f"{player_name} の手を入力 [g/c/p]（g=グー, c=チョキ, p=パー）: ").strip()
    if raw.startswith(":"):
        return None
    return Hand.from_input(raw)


def cpu_pick() -> Hand:
    return choice([Hand.ROCK, Hand.SCISSORS, Hand.PAPER])


def print_status(p1: Player, p2: Player, rules: Rules) -> None:
    console.print(
        f"[info]\nStatus[/]: "
        f"[bold]{p1.name}[/]: {p1.points}pt / {p1.consumed_kcal}/{p1.max_kcal}kcal | "
        f"[bold]{p2.name}[/]: {p2.points}pt / {p2.consumed_kcal}/{p2.max_kcal}kcal | "
        f"target=[bold]{rules.target_points}[/]\n"
    )


def print_rules(rules: Rules) -> None:
    console.print("\n[rule]Rules[/rule]:")
    console.print(f"- target points: [bold]{rules.target_points}[/]")
    console.print(
        f"- tie: [bold]{'both eat own food' if rules.tie_rule_both_eat else 'rematch'}[/]\n"
    )


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


EMOJI = {
    Hand.ROCK: "✊",
    Hand.SCISSORS: "✌️",
    Hand.PAPER: "✋",
}


def _hand_label(hand: Hand, lang: str) -> str:
    if lang == "en":
        names = {Hand.ROCK: "Rock", Hand.SCISSORS: "Scissors", Hand.PAPER: "Paper"}
    else:
        names = {Hand.ROCK: "グー", Hand.SCISSORS: "チョキ", Hand.PAPER: "パー"}
    return f"{names[hand]} {EMOJI[hand]}"


def interactive_loop(
    p1: Player,
    p2: Player,
    rules: Rules,
    mode: str,
    input_mode: str,
    anim_enabled: bool = True,
    anim_interval: float = 1.0,
    language: str = "ja",
) -> int:
    console.print("\n[rule]コマンド: :help / :status / :rules / :quit[/rule]")
    round_no = 1
    while True:
        console.print(f"[rule]--- Round {round_no} ---[/rule]")
        p1_hand: Optional[Hand] = None
        p2_hand: Optional[Hand] = None

        # P1 input
        while p1_hand is None:
            if input_mode == "menu":
                sel = pick_hand_menu(p1.name)
                if sel is None:
                    console.print("[info]Bye![/]")
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
                    console.print("[info]Bye![/]")
                    return 0
                if raw in {":status", ":s"}:
                    print_status(p1, p2, rules)
                    continue
                if raw in {":rules", ":r"}:
                    print_rules(rules)
                    continue
                if raw in {":help", ":h"}:
                    console.print(
                        "\n[info]:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。[/]\n"
                    )
                    continue
                # Otherwise, treat original input as invalid
                console.print("[warning]無効な入力です。 g/c/p または :help を入力してください。[/]")

        # P2 input / CPU
        if mode == "1p":
            p2_hand = cpu_pick()
            console.print(f"[info]{p2.name} は手を選びました。[/]")
        else:
            while p2_hand is None:
                if input_mode == "menu":
                    sel2 = pick_hand_menu(p2.name)
                    if sel2 is None:
                        console.print("[info]Bye![/]")
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
                            console.print("[info]Bye![/]")
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
                            console.print(
                                "\n[info]:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。[/]\n"
                            )
                            p2_hand = None
                            continue
                        console.print("[warning]無効な入力です。 g/c/p または :help を入力してください。[/]")

        # Confirm then animate Janken
        def show(h: Hand) -> str:
            return _hand_label(h, language)
        # Confirmation step
        while True:
            console.print(f"[info]選択中: [bold]{p1.name}[/]: {show(p1_hand)} vs [bold]{p2.name}[/]: {show(p2_hand)}")
            confirmed = False
            if input_mode == "menu":
                sel = questionary.select(
                    "この内容でよろしいですか？" if language != "en" else "Confirm these hands?",
                    choices=[
                        questionary.Choice("決定" if language != "en" else "Confirm", "ok"),
                        questionary.Choice("やり直し" if language != "en" else "Redo", "redo"),
                    ],
                    default="ok",
                ).ask()
                confirmed = (sel == "ok")
            else:
                ans = input("確認しますか？ (y/n) [y]: " if language != "en" else "Confirm? (y/n) [y]: ").strip().lower() or "y"
                confirmed = ans in {"y", "yes"}
            if confirmed:
                break
            # re-pick both hands
            p1_hand = None
            p2_hand = None
            # restart loop for this round
            # P1
            while p1_hand is None:
                if input_mode == "menu":
                    sel = pick_hand_menu(p1.name)
                    if sel is None:
                        console.print("[info]Bye![/]")
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
                    raw = input(":command> ").strip().lower()
                    if raw in {":quit", ":q", ":exit"}:
                        console.print("[info]Bye![/]")
                        return 0
                    if raw in {":status", ":s"}:
                        print_status(p1, p2, rules)
                        continue
                    if raw in {":rules", ":r"}:
                        print_rules(rules)
                        continue
                    if raw in {":help", ":h"}:
                        console.print(
                            "\n[info]:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。[/]\n"
                        )
                        continue
                    console.print("[warning]無効な入力です。 g/c/p または :help を入力してください。[/]")
            # P2
            if mode == "1p":
                p2_hand = cpu_pick()
                console.print(f"[info]{p2.name} は手を選びました。[/]")
            else:
                while p2_hand is None:
                    if input_mode == "menu":
                        sel2 = pick_hand_menu(p2.name)
                        if sel2 is None:
                            console.print("[info]Bye![/]")
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
                                console.print("[info]Bye![/]")
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
                                console.print(
                                    "\n[info]:help, :status, :rules, :quit を利用できます。 もう一度手を入力してください。[/]\n"
                                )
                                p2_hand = None
                                continue
                            console.print("[warning]無効な入力です。 g/c/p または :help を入力してください。[/]")

        # Janken animation (configurable interval): ジャン -> ケン -> ポン！
        if anim_enabled:
            console.print("[info]ジャン…[/]" if language != "en" else "[info]Jan…[/]")
            sleep(anim_interval)
            console.print("[info]ケン…[/]" if language != "en" else "[info]Ken…[/]")
            sleep(anim_interval)
            console.print("[title]ポン！[/]" if language != "en" else "[title]Pon![/]")
            sleep(0.2)
        else:
            console.print("[title]ポン！[/]" if language != "en" else "[title]Pon![/]")

        console.print(f"\n[bold]{p1.name}[/]: {show(p1_hand)} vs [bold]{p2.name}[/]: {show(p2_hand)}")
        result: RoundResult = play_round(p1, p2, p1_hand, p2_hand, rules)
        if result.tie:
            console.print("[tie]勝敗判定: あいこ[/]" if language != "en" else "[tie]Result: Tie[/]")
        else:
            assert result.winner and result.winner_food
            console.print(
                (
                    f"[success]勝敗判定: 勝者 {result.winner.name}[/] (+[success]{result.winner_gained_points}pt[/]) "
                    f"/ 敗者は『{result.winner_food.name}』を食べて [error]+{result.loser_added_kcal}kcal[/]"
                )
                if language != "en"
                else (
                    f"[success]Result: Winner {result.winner.name}[/] (+[success]{result.winner_gained_points}pt[/]) "
                    f"/ Loser eats '{result.winner_food.name}' [error]+{result.loser_added_kcal}kcal[/]"
                )
            )
        print_status(p1, p2, rules)

        over, champion = is_game_over(p1, p2, rules)
        if over:
            console.print(f"[success]🏆 勝者: {champion.name}! お疲れさまでした。[/]\n")
            return 0
        round_no += 1
