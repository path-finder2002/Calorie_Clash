from __future__ import annotations

import argparse
import questionary

from .wizard import run_setup_wizard
from .console import console


def _language_menu(ns: argparse.Namespace) -> None:
    lang = getattr(ns, "language", "ja")
    selected = questionary.select(
        "言語 / Language",
        choices=[
            questionary.Choice("日本語 (ja)", "ja"),
            questionary.Choice("English (en)", "en"),
        ],
        default=lang if lang in {"ja", "en"} else "ja",
    ).ask()
    if selected:
        setattr(ns, "language", selected)


def _rules_menu(ns: argparse.Namespace) -> None:
    # Build checkbox list from current settings
    tie = (ns.tie == "bothEat")
    input_menu = (ns.input == "menu")
    items = [
        ("あいこ時に両者が食べる（bothEat）", "tie_both_eat", tie),
        ("入力を選択メニューにする（questionary）", "input_menu", input_menu),
    ]
    selected = questionary.checkbox(
        "ルール設定（チェックで有効化）",
        choices=[questionary.Choice(label, key, checked=checked) for (label, key, checked) in items],
    ).ask() or []

    ns.tie = "bothEat" if "tie_both_eat" in selected else "rematch"
    ns.input = "menu" if "input_menu" in selected else "direct"


def _options_menu(ns: argparse.Namespace) -> None:
    while True:
        choice = questionary.select(
            "オプション",
            choices=[
                questionary.Choice("言語設定 / Language", "lang"),
                questionary.Choice("ルール設定 / Rules", "rules"),
                questionary.Choice("戻る / Back", "back"),
            ],
        ).ask()
        if choice in (None, "back"):
            return
        if choice == "lang":
            _language_menu(ns)
        elif choice == "rules":
            _rules_menu(ns)


def title_screen(ns: argparse.Namespace) -> tuple[bool, argparse.Namespace]:
    """Return (start_game, namespace) after user interaction.

    start_game=False when user chose Exit or cancelled.
    """
    while True:
        console.print("[title]\nCalorie Clash (CLI)[/title]")
        choice = questionary.select(
            "メニュー",
            choices=[
                questionary.Choice("ゲームスタート / Start Game", "start"),
                questionary.Choice("オプション / Options", "options"),
                questionary.Choice("終了 / Exit", "exit"),
            ],
        ).ask()
        if choice is None or choice == "exit":
            console.print("[info]Bye![/]")
            return False, ns
        if choice == "options":
            _options_menu(ns)
            continue
        if choice == "start":
            # Use wizard to configure before start
            ns = run_setup_wizard(ns)
            return True, ns
