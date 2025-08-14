from __future__ import annotations

import questionary
from random import choice
from time import sleep
import hashlib
from secrets import token_hex
from typing import Optional

from ..core.engine import is_game_over, play_round
from ..core.types import Hand, Player, RoundResult, Rules
from .console import console, gauge_bar
from .ui import pointer_symbol, instruction_select, q_select


def prompt_hand(player_name: str) -> Optional[Hand]:
    raw = input(f"{player_name} の手を入力 [g/c/p]（g=グー, c=チョキ, p=パー）: ").strip()
    if raw.startswith(":"):
        return None
    return Hand.from_input(raw)


def cpu_pick() -> Hand:
    return choice([Hand.ROCK, Hand.SCISSORS, Hand.PAPER])


def print_status(p1: Player, p2: Player, rules: Rules) -> None:
    console.line()
    # Player 1
    p1_score_bar = gauge_bar(p1.points, rules.target_points, width=24, color="green")
    p1_full_color = "red" if p1.consumed_kcal / max(1, p1.max_kcal) >= 0.8 else ("yellow" if p1.consumed_kcal else "cyan")
    p1_full_bar = gauge_bar(p1.consumed_kcal, p1.max_kcal, width=24, color=p1_full_color)
    console.print(f"[bold]{p1.name}[/]")
    console.print(f"  Score  {p1.points}/{rules.target_points}  {p1_score_bar}")
    console.print(f"  Full   {p1.consumed_kcal}/{p1.max_kcal} kcal  {p1_full_bar}")
    console.line()
    # Player 2
    p2_score_bar = gauge_bar(p2.points, rules.target_points, width=24, color="green")
    p2_full_color = "red" if p2.consumed_kcal / max(1, p2.max_kcal) >= 0.8 else ("yellow" if p2.consumed_kcal else "cyan")
    p2_full_bar = gauge_bar(p2.consumed_kcal, p2.max_kcal, width=24, color=p2_full_color)
    console.print(f"[bold]{p2.name}[/]")
    console.print(f"  Score  {p2.points}/{rules.target_points}  {p2_score_bar}")
    console.print(f"  Full   {p2.consumed_kcal}/{p2.max_kcal} kcal  {p2_full_bar}")
    console.line()


def print_rules(rules: Rules) -> None:
    console.line()
    console.print("[rule]Rules[/rule]:")
    console.print(f"- target points: [bold]{rules.target_points}[/]")
    console.print(f"- tie: [bold]{'both eat own food' if rules.tie_rule_both_eat else 'rematch'}[/]")
    console.line()


def pick_hand_menu(player_name: str, ns) -> Optional[Hand]:
    sel = q_select(
        f"{player_name} の手を選んでください",
        choices=[
            questionary.Choice("グー (g)", Hand.ROCK),
            questionary.Choice("チョキ (c)", Hand.SCISSORS),
            questionary.Choice("パー (p)", Hand.PAPER),
            questionary.Separator(" "),
            questionary.Choice("— ステータスを表示 —", "status"),
            questionary.Separator(" "),
            questionary.Choice("— ルールを表示 —", "rules"),
            questionary.Separator(" "),
            questionary.Choice("— 終了 —", "quit"),
        ],
        ns=ns,
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


def _commit_for(name: str, hand: Hand) -> tuple[str, str]:
    """Create a commitment for (name, hand) using a random nonce.

    Returns (commit_hex, nonce). Hash = sha256(nonce + name + ':' + hand_key)
    """
    nonce = token_hex(8)
    hand_key = {Hand.ROCK: "ROCK", Hand.SCISSORS: "SCISSORS", Hand.PAPER: "PAPER"}[hand]
    payload = f"{nonce}{name}:{hand_key}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return digest, nonce


def interactive_loop(
    p1: Player,
    p2: Player,
    rules: Rules,
    mode: str,
    input_mode: str,
    anim_enabled: bool = True,
    anim_interval: float = 1.0,
    language: str = "ja",
    pointer_code: str = "tri",
    pointer_color: str = "magenta",
    underline_color: str = "cyan",
    foods=None,
) -> int:
    console.line()
    console.print("[rule]コマンド: :help / :status / :rules / :quit[/rule]")
    console.line()
    # Show start banner and wait 3 seconds before enabling selection
    console.print("[title]Game Start.[/]")
    sleep(3)
    console.line()
    round_no = 1
    while True:
        console.print(f"[rule]--- Round {round_no} ---[/rule]")
        console.line()
        p1_hand: Optional[Hand] = None
        p2_hand: Optional[Hand] = None
        p1_commit: Optional[tuple[str, str]] = None  # (hash, nonce)
        p2_commit: Optional[tuple[str, str]] = None
        pointer = pointer_symbol(pointer_code)
        # namespace object for UI helpers
        from types import SimpleNamespace
        ui_ns = SimpleNamespace(
            pointer=pointer_code,
            language=language,
            pointer_color=pointer_color,
            underline_color=underline_color,
        )

        # P1 input
        while p1_hand is None:
            if input_mode == "menu":
                sel = pick_hand_menu(p1.name, ui_ns)
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
                if mode == "2p":
                    p1_commit = _commit_for(p1.name, p1_hand)
                    ch = p1_commit[0][:12]
                    msg = (
                        f"[info]{p1.name} のコミットメント: {ch}…[/]"
                        if language != "en"
                        else f"[info]{p1.name} commitment: {ch}…[/]"
                    )
                    console.print(msg)
            else:
                h = prompt_hand(p1.name)
                if h is not None:
                    p1_hand = h
                    if mode == "2p":
                        p1_commit = _commit_for(p1.name, p1_hand)
                        ch = p1_commit[0][:12]
                        msg = (
                            f"[info]{p1.name} のコミットメント: {ch}…[/]"
                            if language != "en"
                            else f"[info]{p1.name} commitment: {ch}…[/]"
                        )
                        console.print(msg)
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
            # CPU commitment (revealed later)
            p2_commit = _commit_for(p2.name, p2_hand)
            ch = p2_commit[0][:12]
            msg = (
                f"[info]{p2.name} のコミットメント: {ch}…（後で公開）[/]"
                if language != "en"
                else f"[info]{p2.name} commitment: {ch}… (salt revealed later)"
            )
            console.print(msg)
        else:
            while p2_hand is None:
                if input_mode == "menu":
                    sel2 = pick_hand_menu(p2.name, ui_ns)
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
                    p2_commit = _commit_for(p2.name, p2_hand)
                    ch = p2_commit[0][:12]
                    msg = (
                        f"[info]{p2.name} のコミットメント: {ch}…[/]"
                        if language != "en"
                        else f"[info]{p2.name} commitment: {ch}…[/]"
                    )
                    console.print(msg)
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
                sel = q_select(
                    "この内容でよろしいですか？" if language != "en" else "Confirm these hands?",
                    choices=[
                        questionary.Choice("決定" if language != "en" else "Confirm", "ok"),
                        questionary.Choice("やり直し" if language != "en" else "Redo", "redo"),
                    ],
                    ns=ui_ns,
                    default="ok",
                ).ask()
                if sel is None:
                    console.print("[info]Bye![/]")
                    return 0
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
                    sel = pick_hand_menu(p1.name, ui_ns)
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
                        sel2 = pick_hand_menu(p2.name, ui_ns)
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
            console.line()
            console.print("[info]ジャン…[/]" if language != "en" else "[info]Jan…[/]")
            sleep(anim_interval)
            console.print("[info]ケン…[/]" if language != "en" else "[info]Ken…[/]")
            sleep(anim_interval)
            console.print("[title]ポン！[/]" if language != "en" else "[title]Pon![/]")
            sleep(0.2)
        else:
            console.print("[title]ポン！[/]" if language != "en" else "[title]Pon![/]")

        console.line()
        console.print(f"[bold]{p1.name}[/]: {show(p1_hand)} vs [bold]{p2.name}[/]: {show(p2_hand)}")
        if foods is not None:
            result: RoundResult = play_round(p1, p2, p1_hand, p2_hand, rules, foods)
        else:
            result = play_round(p1, p2, p1_hand, p2_hand, rules)
        # Delay result log for readability
        sleep(1)
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
            # Additional short cheer line
            winline = (
                f"{result.winner.name}の勝ち！" if language != "en" else f"{result.winner.name} wins!"
            )
            console.print(f"[success]{winline}[/]")
        # Reveal salts
        if mode == "2p":
            if p1_commit:
                console.print(f"[rule]{p1.name} salt: {p1_commit[1]}[/]")
            if p2_commit:
                console.print(f"[rule]{p2.name} salt: {p2_commit[1]}[/]")
        else:
            if p2_commit:
                console.print(f"[rule]{p2.name} salt: {p2_commit[1]}[/]")
        console.line()
        # Delay status gauge output for readability
        sleep(1)
        print_status(p1, p2, rules)

        over, champion = is_game_over(p1, p2, rules)
        if over:
            console.line()
            console.print(f"[success]🏆 勝者: {champion.name}! お疲れさまでした。[/]")
            console.line()
            return 0
        round_no += 1
