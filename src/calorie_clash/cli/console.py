from __future__ import annotations

from rich.console import Console
from rich.theme import Theme


_theme = Theme(
    {
        "title": "bold magenta",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",
        "tie": "bold blue",
        "rule": "dim",
    }
)


console = Console(theme=_theme)


def gauge_bar(current: int | float, maximum: int | float, width: int = 20, color: str = "green") -> str:
    """Return a simple colored gauge bar string like [██████··········].

    - current/maximum are clamped to [0, maximum].
    - color is a Rich markup color name (e.g., 'green', 'yellow', 'red', 'cyan').
    """
    try:
        max_v = max(1.0, float(maximum))
        cur_v = max(0.0, min(float(current), max_v))
    except Exception:
        max_v, cur_v = 1.0, 0.0
    fill = int(round(width * (cur_v / max_v)))
    fill = max(0, min(width, fill))
    filled = "█" * fill
    empty = "·" * (width - fill)
    return f"[{color}]{filled}[/]{empty}"
