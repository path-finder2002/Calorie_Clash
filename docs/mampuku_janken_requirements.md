# 満腹じゃんけんCLIゲーム 要件定義書

## 1. プロジェクト概要

- **名称**: 満腹じゃんけん CLI（英語名: Calorie Clash）
- **目的**: CLI上でプレイできる「満腹じゃんけん」ゲームをTypeScriptで実装し、1P/2P対応、オプション選択機能、カスタマイズ性を備える
- **利用対象**: 開発者・OSSコミュニティ・ゲーム配信者
- **開発言語**: TypeScript (Node.js)

## 2. ゲーム仕様

### 2.1 基本ルール

- ジャンケン（グー・チョキ・パー）で対戦
- 勝者は自分の出した手に紐づく食べ物のポイントを加算
- 敗者は勝者の食べ物を制限時間内に「食べた」としてカロリーを加算
- 勝利条件:
  1. 50ポイント先取
  2. 相手の満腹ゲージ（kcal）が上限に達する

### 2.2 食べ物データ

- 食べ物は「グ・チ・パ」の頭文字ごとに配列で管理
- データ項目: `name`, `points`（文字数ポイント）, `kcal`（満腹ゲージ増加量）
- ユーザーが簡単に追加・編集可能

### 2.3 キャラクター

- 各キャラに以下のパラメータ:
  - `maxKcal`: 満腹ゲージの上限値
  - `jankenSkill`: CPUが強い手を選ぶ確率（0〜1）
  - `bluffResist`: ブラフへの耐性（今後拡張用）

### 2.4 モード

- 1Pモード: プレイヤー vs CPU
- 2Pモード: プレイヤー vs プレイヤー
- CPUはランダムまたは難易度設定に応じた手を出す

### 2.5 入力方式

- デフォルト: g/c/p のキー入力
- オプション: 番号選択形式（`--input=choice`）

### 2.6 カスタムルール設定

- ゲーム開始時または設定画面で以下を変更可能:
  - 目標ポイント（例: 30 / 50 / 70）
  - 満腹ゲージ上限（倍率指定）
  - CPU難易度（スキル値設定）
  - 食べ物リストの差し替え（外部JSON/CSV読み込み）
  - 特殊ルール（例: 勝者が食べる、引き分け時両者食べる 等）

## 3. 機能要件

1. **名前入力**: プレイヤー名、CPU名（任意）を設定可能
2. **キャラ選択**: 上限カロリーやスキルが異なるキャラを選択可能
3. **勝敗判定**: ジャンケン結果に基づきポイント/カロリーを更新
4. **終了条件判定**: ポイントまたは満腹ゲージ到達でゲーム終了
5. **モード選択**: 1P/2P切り替え
6. **オプション入力切替**: CLI引数で入力方式を切り替え
7. **食べ物/キャラデータ編集**: コード内定義を容易に変更可能
8. **カスタムルール**: 設定ファイル/CLI/GUIからゲームルールを変更可能（目標ポイント、満腹倍率、時間制限、デッキ方式 ほか）
9. **プリセット**: Classic/Endurance/Speedrun/Chaos などの定義と選択
10. **検証と既定復帰**: 不正な設定は起動時に検出し、既定値へフォールバック

## 4. 非機能要件

- **可搬性**: Node.js環境で動作（バージョン18以上）
- **拡張性**: 新しいモードやルールを追加しやすい構造
- **可読性**: 関数単位で役割が明確なコード構成
- **ドキュメント整備**: README, GAME_RULES.md, ライセンス, AIエージェント別利用ガイド

## 5. ファイル構成（例）

```
/ (プロジェクトルート)
  ├─ src/
  │   └─ main.ts
  ├─ docs/
  │   ├─ GAME_RULES.md
  │   ├─ GPT.md
  │   ├─ CLAUDE.md
  │   ├─ GEMINI.md
  ├─ README.md
  ├─ LICENSE
  ├─ package.json
  ├─ tsconfig.json
```

## 6. ライセンス

- MIT License 推奨（商用利用可・改変可・著作権表示必須）

## 7. 今後の拡張案

- 難易度設定（CPUのスキル値調整）
- 食べ物リスト外部ファイル読み込み（JSON/CSV）
- オンライン対戦（WebSocket）
- 結果リプレイ保存
- SEや色付きCLI出力
- **カスタムルール一式**（設定ファイル/プリセット/検証/スナップショット）

## 8. カスタムルール仕様

### 8.1 目的
- ルールを**安全に可変**に。バランス検証と配信用に最適化。

### 8.2 設定手段（優先順位）
1. **CLI引数**（最優先）
2. **設定ファイル** `config.json` / `config.yaml`
3. **既定値**（ビルトイン）
> GUI版では「設定」画面から同項目を編集し、`config.json`へ保存。

### 8.3 設定項目一覧（キー / 型 / 既定 / 範囲）
- `targetPoints` / number / **50** / 10–200
- `maxKcalMultiplier` / number / **1.0** / 0.5–2.0（キャラ`maxKcal`に乗算）
- `timeLimitSeconds` / number|null / **600** / 30–1800（`null`は無制限）
- `cpuSkill` / number / **0.65** / 0–1
- `tieRule` / "rematch"|"bothEat" / **"rematch"**
- `declarationMode` / "off"|"optional"|"forced" / **"optional"**
- `foodDeckMode` / "uniform"|"weighted"|"curated" / **"uniform"**
- `foodListPath` / string|null / **null**（外部JSON/CSVで差し替え）
- `allowDuplicateFoods` / boolean / **true**
- `suddenDeathAt` / number|null / **null**（例: 40到達後は引き分け無し）
- `handRevealDelayMs` / number / **0** / 0–3000（演出用）

### 8.4 プリセット
- **Classic**: 50pt / 倍率1.0 / あいこ=再戦
- **Endurance**: 70pt / 倍率1.2 / 時間無制限
- **Speedrun**: 30pt / 倍率0.8 / あいこ=両者食べ
- **Chaos**: 50pt / 倍率1.0 / curatedデッキ（高カロリー偏重）

### 8.5 JSONスキーマ（抜粋）
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "targetPoints": {"type": "integer", "minimum": 10, "maximum": 200},
    "maxKcalMultiplier": {"type": "number", "minimum": 0.5, "maximum": 2},
    "timeLimitSeconds": {"type": ["integer","null"], "minimum": 30, "maximum": 1800},
    "cpuSkill": {"type": "number", "minimum": 0, "maximum": 1},
    "tieRule": {"enum": ["rematch","bothEat"]},
    "declarationMode": {"enum": ["off","optional","forced"]},
    "foodDeckMode": {"enum": ["uniform","weighted","curated"]},
    "foodListPath": {"type": ["string","null"]},
    "allowDuplicateFoods": {"type": "boolean"},
    "suddenDeathAt": {"type": ["integer","null"]},
    "handRevealDelayMs": {"type": "integer", "minimum": 0, "maximum": 3000}
  },
  "additionalProperties": false
}
```

### 8.6 CLI引数（例）
```bash
# 目標70点、CPU強、あいこ両食べ
npx tsx src/main.ts --target=70 --cpu=0.8 --tie=bothEat
# プリセット使用
npx tsx src/main.ts --preset=endurance
# 外部データ差し替え
npx tsx src/main.ts --foods=./foods_custom.json
```

### 8.7 検証とエラー処理
- スキーマで**起動時検証**。
- 不正値は警告し**既定へフォールバック**。
- 致命的な欠落（食品0件など）は**起動中止**。

### 8.8 リプレイ互換
- ルールセットの**スナップショット**をリプレイのヘッダへ保存。
- 乱数シードと併記し**決定論的再現**を保証。

### 8.9 GUI設計
- 設定画面に**スライダ/トグル/セレクト**。
- プリセット選択 → 値が**ライブ反映**。
- 不正値は**赤ハイライト**+ツールチップでガイド。

### 8.10 互換性とバージョニング
- `rulesetVersion` を付与。**SemVer**で管理。
- 旧フォーマットは**マイグレーター**で自動変換。

## 今後の展望

### 7.1 ロードマップ（CLI → GUI → オンライン）
- **短期（0〜3ヶ月）**
  - CLI機能の安定化・分離：`core`ロジックを関数群として独立
  - **GUI PoC**（Tauri + React + Vite）
    - 画面: タイトル / モード選択 / 名前・キャラ選択 / 対戦 / 結果
    - コンポーネント: `HandPicker`, `FoodCard`, `GaugeFullness`, `PointBoard`, `BattleLog`
  - 設定画面の導入：目標ポイント/満腹倍率/CPU強さ/入力方式/特殊ルール
  - **i18n**（ja/en）と文言辞書化
  - 品質: ESLint + Prettier + Vitest（ユニット）

- **中期（3〜6ヶ月）**
  - オンライン対戦（WebSocket）
    - マッチメイキング（フレンド/ランダム）
    - 同期方式: サーバ主導＋**決定論的リプレイ**のための乱数シード共有
  - **リプレイ保存/再生**（JSON + シード）
  - データ外部化：食べ物/キャラを **JSON/CSV** から読み込み
  - **Mod/拡張**: 外部JSONのドラッグ&ドロップで取り込み
  - アクセシビリティ: `aria-*`、コントラスト、`prefers-reduced-motion`
  - 配布: Tauriビルド（macOS/Windows/Linux）

- **長期（6〜12ヶ月）**
  - ランキング/戦績（Elo/レート）
  - デイリーチャレンジ & 限定ルール
  - スキン/テーマ（ダーク/ハイコントラスト）
  - AI連携（GPT/Claude/Gemini）
    - 戦略解析、テストケース自動生成、翻訳
  - モバイル検討（Capacitor）

### 7.2 成功指標（KPI）
- GitHub Stars / Issuesの解決速度
- GUI版の**日次起動数**・**平均対戦数**
- オンライン対戦の**完走率**・**同期失敗率**
- クラッシュ率（Sentry等）
- 改造数（外部JSON/PRの数）

### 7.3 リスクと対策
- **権利面**: 料理名・画像・効果音 → 抽象アイコン化/ライセンス管理
- **同期**: ネット対戦の遅延・ズレ → サーバ主導＋リプレイ検証
- **複雑化**: 機能増で肥大 → `core`/`ui`/`net` の分離と自動テスト
- **多言語**: 文言の分散 → 辞書一元管理とCIで未訳検出

### 7.4 ドキュメント拡充
- `docs/ARCHITECTURE.md`（層と依存関係図）
- `docs/GUI_DESIGN.md`（画面・状態・トランジション）
- `docs/NETPLAY.md`（同期仕様・リプレイ仕様）
- `docs/DATA_FORMAT.md`（JSON/CSVスキーマ）
- `docs/CONFIG.md`（カスタムルール、プリセット、優先順位、スキーマ、例）
- `docs/PRESETS.md`（Classic/Endurance/Speedrun/Chaos の詳細）
- `GPT.md` / `CLAUDE.md` / `GEMINI.md`（AI活用ガイド）

### 7.5 配布・運用
- リリース: GitHub Actionsでマトリクスビルド
- パッケージ: Homebrew Tap / winget / AppImage
- テレメトリ（**任意参加**）: 起動回数・クラッシュのみ収集

> **一言で要約**: コアを固め、GUIへ展開し、オンラインとカスタムルールで伸ばす。

