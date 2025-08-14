from __future__ import annotations

import questionary
from typing import Any, Sequence


POINTER_MAP = {
    "tri": "❯",
    "gt": ">",
    "hand": "👉",
}


def pointer_symbol(code: str | None) -> str:
    return POINTER_MAP.get(code or "tri", "❯")


def instruction_select(language: str) -> str:
    return (
        "↑/↓: 移動 • Enter: 決定 • Esc: キャンセル"
        if language != "en"
        else "↑/↓: Move • Enter: Select • Esc: Cancel"
    )


def instruction_checkbox(language: str) -> str:
    return (
        "↑/↓: 移動 • Space: 切替 • Enter: 確定 • Esc: キャンセル"
        if language != "en"
        else "↑/↓: Move • Space: Toggle • Enter: Apply • Esc: Cancel"
    )


def q_select(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    lang = getattr(ns, "language", "ja")
    kwargs.setdefault("instruction", instruction_select(lang))
    return questionary.select(message, choices=choices, pointer=ptr, **kwargs)


def q_checkbox(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    lang = getattr(ns, "language", "ja")
    kwargs.setdefault("instruction", instruction_checkbox(lang))
    return questionary.checkbox(message, choices=choices, pointer=ptr, **kwargs)
