from __future__ import annotations

import argparse
import questionary
from .ui import pointer_symbol, instruction_select, q_select


def run_setup_wizard(ns: argparse.Namespace) -> argparse.Namespace:
    print("\nセットアップウィザードを開始します。↑/↓で選択、Enterで決定。\n")
    mode = q_select(
        "モードを選択してください",
        choices=[
            questionary.Choice("1P（vs CPU）", "1p"),
            questionary.Choice("2P（vs Player）", "2p"),
        ],
        ns=ns,
        default=ns.mode,
    ).ask()
    if mode is None:
        return ns  # Esc cancels wizard

    # Common: tie rule
    tie = q_select(
        "あいこ時の挙動",
        choices=[
            questionary.Choice("再戦（rematch）", "rematch"),
            questionary.Choice("両者食べる（bothEat）", "bothEat"),
        ],
        ns=ns,
        default=ns.tie,
    ).ask()
    if tie is None:
        return ns

    # Target points
    def _validate_int(val: str):
        try:
            v = int(val)
            return v > 0 or "正の整数を入力してください"
        except Exception:
            return "整数を入力してください"

    target_s = questionary.text("目標ポイント (default 50)", default=str(ns.target), validate=_validate_int).ask()
    target = int(target_s) if target_s else ns.target

    input_mode = q_select(
        "入力方式を選択してください",
        choices=[
            questionary.Choice("選択メニュー（questionary）", "menu"),
            questionary.Choice("直接入力（g/c/p）", "direct"),
        ],
        ns=ns,
        default=ns.input,
    ).ask()
    if input_mode is None:
        return ns

    if mode == "1p":
        p1_name = questionary.text("P1 の名前", default=ns.p1_name).ask() or ns.p1_name
        p2_name = questionary.text("CPU の名前", default=ns.p2_name).ask() or ns.p2_name
        physique = q_select(
            "体格（容量プリセット）",
            choices=[
                questionary.Choice("small (80)", "small"),
                questionary.Choice("medium (100)", "medium"),
                questionary.Choice("large (130)", "large"),
            ],
            ns=ns,
            default=ns.physique,
        ).ask()
        if physique is None:
            return ns
        ns.mode, ns.tie, ns.target, ns.input = mode, tie, target, input_mode
        ns.p1_name, ns.p2_name, ns.physique = p1_name, p2_name, physique
        return ns
    else:
        p1_name = questionary.text("P1 の名前", default=ns.p1_name).ask() or ns.p1_name
        p2_name = questionary.text("P2 の名前", default="P2").ask() or "P2"
        p1_phys = q_select(
            "P1 の体格",
            choices=[
                questionary.Choice("small (80)", "small"),
                questionary.Choice("medium (100)", "medium"),
                questionary.Choice("large (130)", "large"),
            ],
            ns=ns,
            default=ns.physique,
        ).ask()
        if p1_phys is None:
            return ns
        p2_phys = q_select(
            "P2 の体格",
            choices=[
                questionary.Choice("small (80)", "small"),
                questionary.Choice("medium (100)", "medium"),
                questionary.Choice("large (130)", "large"),
            ],
            ns=ns,
            default=ns.physique,
        ).ask()
        if p2_phys is None:
            return ns
        ns.mode, ns.tie, ns.target, ns.input = mode, tie, target, input_mode
        ns.p1_name, ns.p2_name = p1_name, p2_name
        ns.physique = "medium"  # placeholder for 2p
        ns._p1_physique = p1_phys  # type: ignore[attr-defined]
        ns._p2_physique = p2_phys  # type: ignore[attr-defined]
        return ns
