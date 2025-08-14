# ARCHITECTURE.md / アーキテクチャ概要（Python・Bilingual）

---

## English (Original)

### Overview
This document describes the architecture of the **Hungry Janken (Calorie Clash)** project when implemented in Python. It focuses on a clean, testable core with a thin CLI (and optional TUI) and data driven configuration.

### Layers
1. **Presentation Layer**
   - CLI: Python with `typer` or `click` (arg parsing, commands).
   - Optional TUI: `textual` or `rich` for interactive terminal UI.
2. **Game Logic Layer**
   - Pure functions and dataclasses for core RPS mechanics.
   - Food mapping, kcal/points calculation, tie-rule handling.
   - Rule hooks via strategy functions or small plug-in interfaces.
3. **Data Layer**
   - JSON/CSV datasets for foods and characters.
   - Config via `yaml`/`json` files, validated with `pydantic` (optional).

### Module Structure (proposed)
- `src/calorie_clash/core/` — Game engine (pure logic, dataclasses).
- `src/calorie_clash/cli/` — CLI commands (Typer/Click entrypoints).
- `src/calorie_clash/tui/` — Optional TUI (Textual/Rich components).
- `src/calorie_clash/data/` — Embedded defaults and loaders.
- `src/calorie_clash/config/` — Config schemas and parsing helpers.
- `tests/` — Pytest suites for core and I/O seams.

### Configuration & Extensibility
- Rules defined in `config/*.yaml` or `config/*.json`.
- Foods/characters in `data/*.json` or `data/*.csv`.
- Extension points:
  - Custom tie behavior via strategy function registry.
  - Alternate scoring via pluggable calculators.
  - New modes exposed as subcommands (e.g., `calorie-clash tutorial`).

### Packaging & Tooling
- Packaging: `pyproject.toml` with `hatchling`/`setuptools`.
- Dev tools (recommended): `ruff` (lint), `black` (format), `mypy` (types), `pytest` (tests), `tox` or `nox` (optional automation).
- Virtual env: `uv venv` or `python -m venv .venv`.

### Future Expansion
- Multiplayer over WebSocket/HTTP (e.g., `fastapi` backend).
- Save/load profiles (JSON files) and replays.
- AI opponents (rule-based first, then ML if needed).

---

## 日本語（参考訳）

### 概要
本ドキュメントは、**Hungry Janken（Calorie Clash）** を Python で実装する場合のアーキテクチャを示します。薄いCLI（および任意のTUI）と、テストしやすいコアロジック、データ駆動の設定を重視します。

### レイヤー構成
1. **プレゼンテーション層**
   - CLI: `typer` または `click` によるコマンド実装。
   - 任意のTUI: `textual` / `rich` を用いた対話UI。
2. **ゲームロジック層**
   - じゃんけんの基本処理を関数 + `dataclasses` で実装。
   - 食べ物マッピング、kcal/ポイント計算、あいこ挙動。
   - ストラテジ関数や小さなプラグインIFで拡張可能。
3. **データ層**
   - 食べ物・キャラクターは JSON/CSV で管理。
   - 設定は `yaml/json`（必要に応じて `pydantic` でバリデーション）。

### モジュール構造（提案）
- `src/calorie_clash/core/` — ゲームエンジン（純粋ロジック, dataclass）。
- `src/calorie_clash/cli/` — CLIコマンド（Typer/Click のエントリ）。
- `src/calorie_clash/tui/` — 任意のTUI（Textual/Rich）。
- `src/calorie_clash/data/` — デフォルトデータとローダー。
- `src/calorie_clash/config/` — 設定スキーマとパーサ。
- `tests/` — Pytest によるテスト群。

### 設定と拡張
- ルール: `config/*.yaml` / `config/*.json` に定義。
- 食べ物/キャラ: `data/*.json` / `data/*.csv` で管理。
- 拡張ポイント:
  - あいこ時の挙動をストラテジで差し替え。
  - スコア計算を関数差し替えで変更。
  - 新モードはサブコマンドとして追加（例: `calorie-clash tutorial`）。

### パッケージングとツール
- パッケージ: `pyproject.toml`（`hatchling` または `setuptools`）。
- 開発ツール（推奨）: `ruff`（Lint）, `black`（整形）, `mypy`（型）, `pytest`（テスト）, `tox/nox`（任意）。
- 仮想環境: `uv venv` または `python -m venv .venv`。

### 将来拡張
- WebSocket/HTTP によるマルチプレイ（例: `fastapi`）。
- プロファイル保存（JSON）やリプレイ機能。
- AI対戦（ルールベース→必要に応じて機械学習）。

> ※この日本語訳は参考用であり、正式な設計情報は英語版を優先します。
