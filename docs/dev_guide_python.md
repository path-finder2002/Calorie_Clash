# DEV_GUIDE_PYTHON.md / 開発ガイド（Python・Bilingual）

---

## English (Original)

### Prerequisites
- Python 3.11+ (recommended) and Git
- Virtual env tool: `uv` or built-in `venv`

### Setup
```bash
# create & activate venv
uv venv  # or: python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# install tooling (if pyproject not provided yet)
pip install -U pip
pip install black ruff mypy pytest
```

### Project Layout (proposed)
```
src/
  calorie_clash/
    core/      # pure logic
    cli/       # Typer/Click commands
    tui/       # optional Textual/Rich UI
    data/      # default datasets and loaders
    config/    # schemas & parsers

tests/         # pytest suites
```

### Common Tasks
- Format: `black src tests`
- Lint: `ruff check src tests`
- Type-check: `mypy src`
- Run tests: `pytest -q`

### Release (example with setuptools/hatch)
- Build: `python -m build` or `hatch build`
- Local install: `pip install dist/*.whl`

---

## 日本語（参考訳）

### 前提条件
- Python 3.11+ 推奨 / Git
- 仮想環境: `uv` または標準の `venv`

### セットアップ
```bash
# 仮想環境の作成と有効化
uv venv  # または: python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# ツール導入（pyproject が未整備の場合）
pip install -U pip
pip install black ruff mypy pytest
```

### ディレクトリ構成（提案）
```
src/
  calorie_clash/
    core/      # 純粋ロジック
    cli/       # Typer/Click コマンド
    tui/       # 任意の Textual/Rich UI
    data/      # 既定データとローダー
    config/    # スキーマとパーサ

tests/         # pytest テスト群
```

### よく使うコマンド
- 整形: `black src tests`
- Lint: `ruff check src tests`
- 型チェック: `mypy src`
- テスト: `pytest -q`

### リリース（setuptools/hatch の例）
- ビルド: `python -m build` または `hatch build`
- ローカル導入: `pip install dist/*.whl`

