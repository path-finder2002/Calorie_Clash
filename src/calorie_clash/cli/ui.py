from __future__ import annotations

import questionary
from typing import Any, Sequence, Union, Dict


POINTER_MAP = {
    "tri": "❯",
    "gt": ">",
    "hand": "👉",
}


def pointer_symbol(code: str | None) -> str:
    return POINTER_MAP.get(code or "tri", "❯")


def q_select(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    return questionary.select(message, choices=choices, pointer=ptr, **kwargs)


def q_checkbox(message: str, choices: Sequence, ns, **kwargs: Any):
    ptr = pointer_symbol(getattr(ns, "pointer", "tri"))
    return questionary.checkbox(message, choices=choices, pointer=ptr, **kwargs)

