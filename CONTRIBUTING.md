# Contributing

Rainkeeper is a solo-maintained project by [@simonives](https://github.com/simonives).

## Bug reports

Use the [bug report template](https://github.com/simonives/rainkeeper/issues/new?template=bug_report.md).

The most useful reports include:
- Which tool you called and with what parameters
- What you expected vs what actually happened
- Whether the issue is reproducible
- Your Raindrop.io account type (free / Pro)

## Feature ideas

Start in [Discussions -> Ideas](https://github.com/simonives/rainkeeper/discussions/categories/ideas) before opening an issue. This gives ideas space to develop and keeps the issue tracker focused on concrete, scoped work. Once an idea is well-defined, it will be promoted to an issue and tracked there.

## Questions

Use [Discussions -> Q&A](https://github.com/simonives/rainkeeper/discussions/categories/q-a) for setup help and usage questions.

## Forks

Fork freely -- MIT licensed. If you build something useful on top of Rainkeeper, share it in [Discussions -> Show and tell](https://github.com/simonives/rainkeeper/discussions).

## Pull requests

This is a solo-maintained project and external PRs are unlikely to be merged. If you have identified a fix, open an issue first so we can agree on scope and approach before you invest the effort. If a fix is accepted, it will be committed by the maintainer.

## Code style

- Python 3.12+
- `ruff check src/` -- no warnings or errors
- Type hints on all public functions
- All HTTP calls through `RaindropClient` -- no `httpx` in tool files
- Tool docstrings describe what the tool does and when to use it; Claude uses these for tool selection
