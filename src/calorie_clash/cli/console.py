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
