from __future__ import annotations

import questionary
from typing import Any, Sequence
from questionary import Style


POINTER_MAP = {
    "tri": "❯",
    "gt": ">",
    "hand": "👉",
}


def pointer_symbol(code: str | None) -> str:
    return POINTER_MAP.get(code or "tri", "❯")


def instruction_select(language: str) -> str:
    return (
        "\n↑/↓: 移動 • Enter: 決定 • ^C: キャンセル\n"
        if language != "en"
        else "\n↑/↓: Move • Enter: Select • ^C: Cancel\n"
    )


def instruction_checkbox(language: str) -> str:
    return (
        "\n↑/↓: 移動 • Space: 切替 • Enter: 確定 • ^C: キャンセル\n"
        if language != "en"
        else "\n↑/↓: Move • Space: Toggle • Enter: Apply • ^C: Cancel\n"
    )


def q_select(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    lang = getattr(ns, "language", "ja")
    kwargs.setdefault("instruction", instruction_select(lang))
    # Build style with pointer color and underline color
    pcolor = getattr(ns, "pointer_color", "magenta")
    ucolor = getattr(ns, "underline_color", "cyan")
    style = Style([
        ("qmark", f"fg:{pcolor} bold"),
        ("pointer", f"fg:{pcolor} bold"),
        ("highlighted", f"fg:{ucolor} underline"),
        ("selected", f"fg:{ucolor} underline"),
        ("instruction", "fg:#888888"),
    ])
    return questionary.select(message, choices=choices, pointer=ptr, style=style, **kwargs)


def q_checkbox(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    lang = getattr(ns, "language", "ja")
    kwargs.setdefault("instruction", instruction_checkbox(lang))
    pcolor = getattr(ns, "pointer_color", "magenta")
    ucolor = getattr(ns, "underline_color", "cyan")
    style = Style([
        ("qmark", f"fg:{pcolor} bold"),
        ("pointer", f"fg:{pcolor} bold"),
        ("highlighted", f"fg:{ucolor} underline"),
        ("selected", f"fg:{ucolor} underline"),
        ("instruction", "fg:#888888"),
    ])
    return questionary.checkbox(message, choices=choices, pointer=ptr, style=style, **kwargs)
