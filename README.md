# SkillBank Agent

An accumulative LLM agent that builds a growing library of reusable Python skills as it solves tasks — inspired by the [Co-Evolving LLM Decision and Skill Bank](https://arxiv.org/abs/2408.08032) paper.

## Concept & Motivation

Most LLM agent demos are stateless: every run starts from zero context. SkillBank makes agents *accumulative*. Each time the agent solves a task, it extracts the reusable building blocks — small, self-contained Python functions — and stores them in a local vector database. On future tasks, semantically similar skills are retrieved and injected as context, letting the agent build on prior solutions rather than rediscovering them.

This mirrors how experienced developers maintain personal utility libraries. The practical result is an agent that demonstrably improves on related task families over time: the more tasks you run, the richer the skill bank, and the better the generated code tends to be. Everything runs locally — no cloud vector DB, no model training, no GPU required.

The skill bank is backed by [ChromaDB](https://www.trychroma.com/) for persistent local storage and [sentence-transformers](https://www.sbert.net/) (MiniLM-L6) for embedding. Code generation and skill extraction use the Claude API (Anthropic). Deduplication prevents redundant entries via cosine-similarity thresholding.

## What Works (M1 — scaffold)

- Python package scaffold under `src/skillbank/` (src layout, `setuptools.build_meta`)
- `pyproject.toml` with pinned dependencies and `[project.scripts]` entry point
- `requirements.txt` and `requirements-dev.txt` for visibility
- `.gitignore` and MIT `LICENSE`
- CLI entry point wired: `skillbank --help` and `skillbank --version` work
- Four command stubs registered (`run`, `list`, `reset`, `demo`) — each raises `Not implemented yet` until M2+
- Draft architecture diagram in `docs/architecture.md`
- `tests/` directory with scaffold smoke test

## CLI Interface

```
Usage: skillbank [OPTIONS] COMMAND [ARGS]...

  SkillBank Agent — accumulative LLM agent with a growing skill library.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  demo   Run 5 canonical demo tasks and print skill-bank growth stats.
  list   List all skills currently stored in the skill bank.
  reset  Clear all skills from the skill bank.
  run    Run TASK using the skill bank, then extract new skills.

Examples:
  # Solve a task (verbose mode shows retrieved skills + generated code)
  skillbank run "parse a CSV and compute column averages" --verbose

  # See what the agent has learned so far
  skillbank list

  # Watch the bank grow across 5 demo tasks
  skillbank demo

  # Start fresh
  skillbank reset
```

> **Note:** `run`, `list`, `reset`, and `demo` raise a "Not implemented yet" error until M2+. Only `--help` and `--version` are functional in this release.

## Quick Start

```bash
# 1. Clone and create a virtual environment
git clone <repo-url>
cd skillbank-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install in editable mode
pip install -e .

# 3. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 4. Verify the CLI is available
skillbank --help
```

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for a diagram of the agent loop.

<!-- TODO: embed inline diagram here once M6 pipeline is complete -->

## Roadmap

| Milestone | Scope | Status |
|-----------|-------|--------|
| M1 | Scaffold: package structure, CLI stubs, architecture draft | **done** |
| M2 | ChromaDB integration, skill store CRUD | planned |
| M3 | Embedding pipeline (MiniLM-L6), skill retrieval | planned |
| M4 | Claude Haiku code generation + skill extraction | planned |
| M5 | Subprocess sandbox execution, feedback loop | planned |
| M6 | Demo suite, benchmarks, full architecture docs | planned |

## License

MIT — see [LICENSE](LICENSE).
