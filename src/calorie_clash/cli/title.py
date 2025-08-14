from __future__ import annotations

import argparse
import questionary

from .wizard import run_setup_wizard
from .console import console
from .ui import pointer_symbol, q_select, q_checkbox, instruction_select, instruction_checkbox


def _language_menu(ns: argparse.Namespace) -> None:
    lang = getattr(ns, "language", "ja")
    selected = q_select(
        "言語 / Language",
        choices=[
            questionary.Choice("日本語 (ja)", "ja"),
            questionary.Choice("English (en)", "en"),
        ],
        ns=ns,
        default=lang if lang in {"ja", "en"} else "ja",
    ).ask()
    if selected:
        setattr(ns, "language", selected)


def _rules_menu(ns: argparse.Namespace) -> None:
    # Build checkbox list from current settings
    tie = (getattr(ns, "tie", "rematch") == "bothEat")
    input_menu = (getattr(ns, "input", "direct") == "menu")
    anim_on = (getattr(ns, "anim", "on") == "on")
    items = [
        ("あいこ時に両者が食べる（bothEat）", "tie_both_eat", tie),
        ("入力を選択メニューにする（questionary）", "input_menu", input_menu),
        ("アニメーションを有効化（ジャン→ケン→ポン）", "anim_on", anim_on),
    ]
    selected = q_checkbox(
        "ルール設定（チェックで有効化）",
        choices=[questionary.Choice(label, key, checked=checked) for (label, key, checked) in items],
        ns=ns,
    ).ask() or []

    ns.tie = "bothEat" if "tie_both_eat" in selected else "rematch"
    ns.input = "menu" if "input_menu" in selected else "direct"
    ns.anim = "on" if "anim_on" in selected else "off"

    # Speed prompt when animation is on
    if ns.anim == "on":
        def _validate_float(val: str):
            try:
                v = float(val)
                return v >= 0 or "0以上の数値を入力してください"
            except Exception:
                return "数値を入力してください"
        current = str(getattr(ns, "anim_speed", 1.0))
        speed = questionary.text("アニメ間隔（秒）", default=current, validate=_validate_float).ask()
        if speed:
            try:
                ns.anim_speed = float(speed)
            except Exception:
                pass


def _options_menu(ns: argparse.Namespace) -> None:
    while True:
        choice = q_select(
            "オプション",
            choices=[
                questionary.Choice("言語設定 / Language", "lang"),
                questionary.Choice("ルール設定 / Rules", "rules"),
                questionary.Choice("カーソル表示 / Cursor", "cursor"),
                questionary.Choice("色設定 / Colors", "colors"),
                questionary.Choice("戻る / Back", "back"),
            ],
            ns=ns,
        ).ask()
        if choice in (None, "back"):
            return
        if choice == "lang":
            _language_menu(ns)
        elif choice == "rules":
            _rules_menu(ns)
        elif choice == "cursor":
            _cursor_menu(ns)
        elif choice == "colors":
            _colors_menu(ns)


def title_screen(ns: argparse.Namespace) -> tuple[bool, argparse.Namespace]:
    """Return (start_game, namespace) after user interaction.

    start_game=False when user chose Exit or cancelled.
    """
    while True:
        console.line()
        console.print("[title]Calorie Clash (CLI)[/title]")
        console.line()
        choice = q_select(
            "メニュー",
            choices=[
                questionary.Choice("ゲームスタート / Start Game", "start"),
                questionary.Choice("オプション / Options", "options"),
                questionary.Choice("終了 / Exit", "exit"),
            ],
            ns=ns,
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


def _cursor_menu(ns: argparse.Namespace) -> None:
    ptr_code = getattr(ns, "pointer", "tri")
    choices = [
        questionary.Choice("❯ (tri)", "tri"),
        questionary.Choice("> (gt)", "gt"),
        questionary.Choice("👉 (hand)", "hand"),
    ]
    selected = q_select(
        "カーソル表示 / Cursor",
        choices=choices,
        ns=ns,
        default=ptr_code,
    ).ask()
    if selected:
        setattr(ns, "pointer", selected)


def _colors_menu(ns: argparse.Namespace) -> None:
    # Predefined safe colors for prompt_toolkit
    color_choices = [
        questionary.Choice("magenta", "magenta"),
        questionary.Choice("cyan", "cyan"),
        questionary.Choice("green", "green"),
        questionary.Choice("yellow", "yellow"),
        questionary.Choice("blue", "blue"),
        questionary.Choice("white", "white"),
    ]
    ptr_color = q_select(
        "カーソル色 / Pointer Color",
        choices=color_choices,
        ns=ns,
        default=getattr(ns, "pointer_color", "magenta"),
    ).ask()
    if ptr_color:
        setattr(ns, "pointer_color", ptr_color)
    ul_color = q_select(
        "選択箇所の下線色 / Underline Color",
        choices=color_choices,
        ns=ns,
        default=getattr(ns, "underline_color", "cyan"),
    ).ask()
    if ul_color:
        setattr(ns, "underline_color", ul_color)
