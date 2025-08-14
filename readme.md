# 満腹じゃんけん CLI / Calorie Clash CLI

> 「勝つか、食べるか。」— TypeScriptで動くジャンケン×大食いCLI

## 概要 / Overview
Node.js 18+ / TypeScript 製のCLIゲームです。1P（vs CPU）/ 2P（vs Player）、カスタムルール（目標ポイント、満腹度容量、時間制限、あいこ時挙動）、入力モード（g/c/p 直入力 or 選択メニュー）に対応。食べ物・キャラクターは拡張可能なデータ構造で管理します。

## インストール / Install
```bash
npm i
```

## 実行 / Run
```bash
npx tsx src/main.ts [--mode=1p|2p|tutorial] [--input=direct|menu] \
  [--target=5] [--capacity=100] [--multiplier=1] \
  [--time=20] [--tie=replay|bothEat|skip] [--physique=small|medium|large] \
  [--p1-name=NAME] [--p2-name=NAME] [--p1-physique=small|medium|large] [--p2-physique=small|medium|large]
```

例: 1P・メニュー入力・あいこで両者食べる
```bash
npx tsx src/main.ts --mode=1p --input=menu --tie=bothEat
```

例: チュートリアルを開始してから通常ゲームへ
```bash
npx tsx src/main.ts --mode=tutorial
```

例: 2P対戦（両者とも人間）
```bash
npx tsx src/main.ts --mode=2p
```

### 体格（容量プリセット）
- `--physique=small|medium|large` で容量をプリセット（small: 80 / medium: 100 / large: 130）。
- 起動時メニューでも体格を選択できます（選択すると `capacity` が上書きされます）。
```bash
npx tsx src/main.ts --mode=1p --physique=large
```

### 名前と個別体格
- 起動時メニューでP1/P2の名前と体格を個別に設定可能。
- CLIからも指定できます。
```bash
npx tsx src/main.ts --mode=2p \
  --p1-name=太郎 --p1-physique=large \
  --p2-name=花子 --p2-physique=small
```

## テスト / Test
```bash
npm test
```

## メニューで使えるコマンド
- `:help` ヘルプ表示
- `:status` 現在のスコア/満腹度を表示
- `:rules` 現在のルールを表示
- `:set key=value` ルール変更（`input=direct|menu`, `time=秒`, `tie=replay|bothEat|skip`, `target=数`, `capacity=数`, `multiplier=数`）
- `:quit` 終了

## 仕組み / Architecture
- ゲームロジック: `src/core/game.ts`
- UI入出力: `src/cli/ui.ts`
- 設定/引数: `src/cli/config.ts`
- データ(食べ物/キャラ): `src/core/data.ts`
- エントリ: `src/main.ts`（薄い） / 実体: `src/cli/main.ts`
- 基本テスト: `src/tests/game.test.ts`

MIT License
