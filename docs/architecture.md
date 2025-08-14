# ARCHITECTURE.md / アーキテクチャ概要（Bilingual）

---

## English (Original)

### Overview
This document describes the architecture of the **Hungry Janken** game project. It includes the CLI prototype, planned GUI version, and customization systems.

### Layers
1. **Presentation Layer**
   - CLI Interface: Node.js (TypeScript) readline-based.
   - Planned GUI: Electron + React, responsive layout.
2. **Game Logic Layer**
   - Core engine for Rock-Scissors-Paper mechanics.
   - Food mapping and kcal/points calculations.
   - Tie rule variations and custom rule hooks.
3. **Data Layer**
   - JSON-based food database with kcal and point values.
   - Character stats and profiles.
   - Configurable via external files.

### Module Structure
- `/src/cli/` — CLI implementation.
- `/src/gui/` — GUI implementation (future).
- `/src/core/` — Game logic engine.
- `/data/` — Food and character datasets.
- `/config/` — Rule and game settings.

### Customization Hooks
- Rule definitions in `/config/rules.json`.
- Character and food definitions in `/data/`.
- Optional plugins for new game modes.

### Future Expansion
- Multiplayer via WebSocket.
- Save/load system.
- AI opponents with difficulty scaling.

---

## 日本語（参考訳）

### 概要
本ドキュメントは、**Hungry Janken** ゲームプロジェクトのアーキテクチャを記述します。CLIプロトタイプ、将来のGUI版、カスタマイズシステムを含みます。

### レイヤー構成
1. **プレゼンテーション層**
   - CLIインターフェース: Node.js（TypeScript）+ readline。
   - GUI予定: Electron + React、レスポンシブ対応。
2. **ゲームロジック層**
   - じゃんけんの基本処理エンジン。
   - 食べ物マッピング、kcal/ポイント計算。
   - あいこルールやカスタムルールのフック。
3. **データ層**
   - kcalとポイント値を含むJSON形式の食べ物データベース。
   - キャラクターの能力値とプロフィール。
   - 外部ファイルから設定可能。

### モジュール構造
- `/src/cli/` — CLI実装。
- `/src/gui/` — GUI実装（将来予定）。
- `/src/core/` — ゲームロジックエンジン。
- `/data/` — 食べ物・キャラクターデータセット。
- `/config/` — ルールや設定ファイル。

### カスタマイズフック
- `/config/rules.json` にルール定義。
- `/data/` にキャラ・食べ物定義。
- 新モード用のプラグインにも対応予定。

### 将来拡張
- WebSocketによるマルチプレイ。
- セーブ/ロード機能。
- 難易度調整付きAI対戦相手。

> ※この日本語訳は参考用であり、正式な設計情報は英語版を優先します。

