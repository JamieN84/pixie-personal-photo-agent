# Repository Guidelines

## Project Structure & Module Organization
- `photo_agent-ai.py` holds the CLI entry point, data models, and orchestration for planning and applying photo moves.
- Audit CSVs named `photo_agent_audit_*.csv` are emitted in the repo root; move long-term logs into `artifacts/` or delete once reviewed.
- The tool expects source and target folders on the filesystem; keep sample fixtures under `samples/` if you add them for testing.

## Build, Test, and Development Commands
- `python -m venv .venv && .\.venv\Scripts\activate` creates an isolated environment; prefer Python 3.11+.
- `pip install pydantic rich requests openai` pulls the current dependencies; pin versions in `requirements.txt` when you add more modules.
- Dry-run organiser: `python photo_agent-ai.py --source <inbox> --target <library> --say "<context>"`.
- To execute moves add `--apply`; always review the audit preview first.
- Undo a previous run with `python photo_agent-ai.py --undo photo_agent_audit_<timestamp>.csv`.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation, type hints, and descriptive snake_case for functions and CLI flags.
- Keep module-level helpers pure and side-effect free; encapsulate CLI-only behavior inside `main()`.
- Format Python with `black` (line length 88) and lint with `ruff` before opening a PR.

## Testing Guidelines
- Adopt `pytest`; organise future tests under `tests/` with filenames `test_*.py`.
- Use temp directories or fixtures to simulate photo trees; assert that planned operations stay below the chosen target root.
- Capture at least one regression test for JSON parsing to catch model drift; run `pytest` locally before pushing.

## Commit & Pull Request Guidelines
- No git history exists yet; start with Conventional Commits (`feat:`, `fix:`, `docs:`) and present-tense summaries.
- PRs should describe the scenario exercised (`--say`, backend, dry-run output) and attach relevant audit snippets.
- Link tracking issues when possible and flag any destructive migrations so reviewers can plan backups.

## Security & Configuration Tips
- Store `OPENAI_API_KEY` and other secrets in your shell profile or a `.env` excluded from version control.
- When testing `--apply`, work on disposable copies of photos and confirm disk quotas before large moves.
- Keep Ollama/OpenAI endpoints reachable; handle network failures gracefully in follow-up changes.
