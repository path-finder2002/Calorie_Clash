# CONTRIBUTING / コントリビューティング（Python・Bilingual）

---

## English (Original)

### How to Contribute
Thank you for your interest in contributing! We welcome:
- Bug reports and feature requests
- Documentation improvements
- Code changes (bug fixes and features)

### Local Development (Python)
1. Fork the repository and clone your fork.
2. Create a virtual environment:
   - `uv venv` (recommended) or `python -m venv .venv`
   - Activate it: `source .venv/bin/activate` (Unix/macOS) or `.venv\\Scripts\\activate` (Windows)
3. Install dev tools (if `pyproject.toml` exists): `pip install -e .[dev]`
   - If not available yet, install directly: `pip install black ruff mypy pytest`
4. Create a feature branch: `git switch -c feat/your-feature`
5. Make changes and run quality checks:
   - Format: `black src tests`
   - Lint: `ruff check src tests`
   - Type-check: `mypy src`
   - Test: `pytest -q`

### Code Guidelines
- Prefer pure functions and dataclasses in `core`.
- Keep I/O, CLI, and parsing thin and isolated.
- Add or update tests for new behavior; keep them deterministic.
- Maintain bilingual docs when possible (EN/JA).

### Pull Requests
1. Ensure formatting, lint, types, and tests pass locally.
2. Write a clear PR title and description (use Conventional Commits if possible).
3. Include steps to verify and, if UI/TUI is affected, screenshots/recordings.

### Communication
- Use GitHub Issues for bugs/ideas.
- Be respectful, constructive, and concise.

---

## 日本語（参考訳）

### 貢献方法
ご関心ありがとうございます。以下の貢献を歓迎します：
- バグ報告／機能要望
- ドキュメント改善
- コード修正（バグ修正・機能追加）

### ローカル開発（Python）
1. リポジトリをフォークしてクローン。
2. 仮想環境を作成：
   - 推奨: `uv venv` または `python -m venv .venv`
   - 有効化: `source .venv/bin/activate`（Unix/macOS）/ `.venv\\Scripts\\activate`（Windows）
3. 開発ツールをインストール（`pyproject.toml` がある場合）: `pip install -e .[dev]`
   - ない場合は個別に: `pip install black ruff mypy pytest`
4. ブランチ作成: `git switch -c feat/your-feature`
5. 変更後の品質チェック：
   - 整形: `black src tests`
   - Lint: `ruff check src tests`
   - 型: `mypy src`
   - テスト: `pytest -q`

### コーディングガイドライン
- `core` は純粋関数 + dataclass を優先。
- I/O・CLI・パースは薄く分離する。
- 新規挙動には必ずテストを追加。決定的に保つ。
- 可能であれば英日バイリンガルでドキュメント更新。

### プルリクエスト
1. 整形・Lint・型・テストをローカルで合格させる。
2. タイトルと概要は明確に（可能なら Conventional Commits）。
3. UI/TUI 変更時は確認手順やスクリーンショット/録画を添付。

### コミュニケーション
- バグ/要望は GitHub Issues を使用。
- 互いに敬意を払い、建設的かつ簡潔に議論する。

> ※この日本語訳は参考用であり、正式な運用指針は英語版を優先します。
