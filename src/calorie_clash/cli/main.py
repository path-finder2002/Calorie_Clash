from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from random import choice
from typing import Optional

from ..core.data import PHYSIQUE_CAPACITY, load_foods_csv
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
    parser.add_argument(
        "--pointer",
        choices=["tri", "gt", "hand"],
        default="tri",
        help="Menu cursor style: tri=❯, gt=>, hand=👉",
    )
    parser.add_argument(
        "--pointer-color",
        choices=["magenta", "cyan", "green", "yellow", "blue", "white"],
        default="magenta",
        help="Pointer color (questionary style)",
    )
    parser.add_argument(
        "--underline-color",
        choices=["cyan", "magenta", "green", "yellow", "blue", "white"],
        default="cyan",
        help="Underline color for highlighted selection",
    )
    parser.add_argument("--foods-csv", default=None, help="Foods CSV path (hand,name,kcal)")
    return parser.parse_args(argv)


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
    # Load foods from options or CLI if provided
    foods = None
    if hasattr(ns, "_foods"):
        foods = getattr(ns, "_foods")
    elif getattr(ns, "foods_csv", None):
        try:
            foods = load_foods_csv(ns.foods_csv)
            console.print(f"[info]Foods CSV loaded: {ns.foods_csv}[/]")
        except Exception as e:
            console.print(f"[warning]Foods CSV load failed: {e}[/]")

    return interactive_loop(
        p1,
        p2,
        rules,
        ns.mode,
        ns.input,
        anim_enabled,
        anim_interval,
        language,
        pointer_code=getattr(ns, "pointer", "tri"),
        pointer_color=getattr(ns, "pointer_color", "magenta"),
        underline_color=getattr(ns, "underline_color", "cyan"),
        foods=foods,
    )


if __name__ == "__main__":
    raise SystemExit(main())
