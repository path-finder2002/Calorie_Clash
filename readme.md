# 満腹じゃんけん CLI / Calorie Clash CLI

> ポイントを稼ぐか、満腹で脱落か──胃袋の限界バトル。

## 概要 / Overview
Python 製の CLI ゲームです。1P（vs CPU）/ 2P（vs Player）、カスタムルール（目標ポイント、満腹度容量、あいこ時挙動）、入力モード（g/c/p 直入力 or questionary による選択メニュー）に対応。
Rich による色付き出力で視認性を高めています。

## インストール / Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
```

## 実行 / Run
```bash
# 引数なしで実行（タイトル画面 → スタート/オプション/終了）
calorie-clash

# 2P 対戦（両者とも人間）
calorie-clash --mode 2p

# questionary による選択メニュー入力
calorie-clash --mode 1p --input menu

# セットアップウィザードで起動（モード/体格/タイールール等を対話設定）
calorie-clash --wizard

# インストールせずに実行（開発時）
PYTHONPATH=src python -m calorie_clash --mode 1p  # Windows: $env:PYTHONPATH="src"; python -m calorie_clash --mode 1p
```

## テスト / Test
（任意）pytest を導入後に追加予定です。

## メニューで使えるコマンド
- `:help` ヘルプ表示
- `:status` 現在のスコア/満腹度を表示
- `:rules` 現在のルールを表示
- `:set key=value` ルール変更（`input=direct|menu`, `time=秒`, `tie=replay|bothEat|skip`, `target=数`, `capacity=数`, `multiplier=数`）
- `:quit` 終了

## アニメーション / 確認
- 決定確認: 双方の手の選択後に「決定/やり直し」を確認
- ジャン・ケン・ポン！: 1秒刻みで表示（ジャン → ケン → ポン！）

## タイトル/オプション
- タイトル: 「ゲームスタート」「オプション」「終了」
- オプション: 
  - 言語設定（ja/en）
  - ルール設定（チェックボックス）
    - あいこ時に両者食べる（bothEat）
    - 入力方式を選択メニュー（questionary）にする

## 仕組み / Architecture
- コア型/データ: `src/calorie_clash/core/types.py`, `src/calorie_clash/core/data.py`
- ゲームロジック: `src/calorie_clash/core/engine.py`
- CLI入出力/進行: `src/calorie_clash/cli/loop.py`
- セットアップウィザード: `src/calorie_clash/cli/wizard.py`
- タイトル/オプション: `src/calorie_clash/cli/title.py`
- エントリ: `src/calorie_clash/cli/main.py` / `src/calorie_clash/__main__.py`
- コンソール（色テーマ）: `src/calorie_clash/cli/console.py`

MIT License

### 主要オプション
- `--mode`: `1p` | `2p`
- `--input`: `direct` | `menu`（questionary）
- `--target`: 目標ポイント（既定 50）
- `--physique`: `small` | `medium` | `large`（満腹上限 80/100/130）
- `--p1-name`, `--p2-name`: プレイヤー名
- `--tie`: `rematch` | `bothEat`（あいこ時の挙動）
- `--wizard`: 起動時にセットアップウィザードを実行
