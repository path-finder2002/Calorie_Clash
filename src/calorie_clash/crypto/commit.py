from __future__ import annotations

import hashlib
from secrets import token_hex
from ..core.types import Hand


def make_commit(name: str, hand: Hand) -> tuple[str, str]:
    nonce = token_hex(8)
    key = {Hand.ROCK: "ROCK", Hand.SCISSORS: "SCISSORS", Hand.PAPER: "PAPER"}[hand]
    payload = f"{nonce}{name}:{key}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return digest, nonce


def verify_commit(name: str, hand: Hand, nonce: str, commit_hex: str) -> bool:
    key = {Hand.ROCK: "ROCK", Hand.SCISSORS: "SCISSORS", Hand.PAPER: "PAPER"}[hand]
    payload = f"{nonce}{name}:{key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest() == commit_hex.lower()


def commit_prefix(commit_hex: str, length: int = 12) -> str:
    return commit_hex[:length]

