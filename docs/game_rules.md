# GAME_RULES.md / ゲームルール（Bilingual）

---

## English (Original)

### Objective
Be the first player to either:
1. Reach the target points (default: 50), **or**
2. Fill your opponent's fullness gauge (reach their max kcal).

### How to Play
- Players choose one of Rock (グー), Scissors (チョキ), or Paper (パー) each round.
- Each hand is linked to a food item starting with that syllable (e.g., "グー" → Gratin).
- The winning player gains points equal to the length-based score of their food.
- The losing player must "eat" the winner's food, adding its kcal to their fullness gauge.

### Tie Rules
- Default: Replay the round (no points, no food eaten).
- Optional: Both players eat their own food (custom rule).

### Victory Conditions
- Reaching the target points first.
- Opponent exceeding their max kcal.

### Characters
- Each character has:
  - **maxKcal**: Fullness gauge limit.
  - **jankenSkill**: Likelihood of choosing a winning hand (CPU only).
  - **bluffResist**: Resistance to declaration bluffs (future expansion).

### Custom Rules
- Adjustable target points, max kcal multiplier, time limit.
- Tie behavior, declaration mode, food deck mode.
- External food/character data via JSON or CSV.

---

## 日本語（参考訳）

### 目的
以下のいずれかを先に達成したプレイヤーが勝利：
1. 目標ポイント（既定: 50）に到達する
2. 相手の満腹ゲージを最大kcalまで満たす

### 遊び方
- 各ラウンドで、プレイヤーはグー・チョキ・パーのいずれかを出す。
- 出した手の頭文字に対応する食べ物が選ばれる（例: 「グー」→ グラタン）。
- 勝者は、その食べ物の文字数ポイントを獲得。
- 敗者は勝者の食べ物を「食べ」、そのkcalが自分の満腹ゲージに加算される。

### あいこのルール
- 既定: 再戦（ポイントもカロリーも変動なし）
- オプション: あいこで出した手のカードはこのターン中は使用禁止（カスタムルール）
- オプション: 両者が自分の食べ物を食べる（カスタムルール）

### 勝利条件
- 先に目標ポイントに到達
- 相手の満腹ゲージが上限を超える

### キャラクター
- 各キャラには以下のパラメータがある：
  - **maxKcal**: 満腹ゲージの上限
  - **jankenSkill**: CPUが勝ちやすい手を選ぶ確率
  - **bluffResist**: 宣言ブラフへの耐性（将来拡張）

### カスタムルール
- 目標ポイント、満腹倍率、時間制限を調整可能
- あいこの挙動、宣言モード、デッキ方式の切替
- JSON/CSVによる外部データの読み込みに対応

> ※この日本語訳は参考用であり、正式なルールは英語版を優先します。

