# econ_research_assistant

A Python CLI tool that helps an economics researcher explore, merge, and analyze datasets. The agent proposes plans and waits for explicit human approval before merging data or running analysis.

## Stack

- Python 3.11+ (conda environment)
- Raw Anthropic Messages API with tool use — no agent framework
- pandas, pyreadstat (Stata `.dta` / SPSS `.sav`), matplotlib + seaborn, pydantic, pytest

## Design principles

**Human control is structural, not behavioral.** The agent cannot merge or analyze without explicit confirmation. Approval gates before merge and analysis are hardcoded — not configurable, not skippable — and logged to `logs/approvals.jsonl` for audit.

- `data/` is read-only; the agent never modifies inputs
- All generated files go to `outputs/` with timestamped filenames
- Stata: write `.do` files only, no programmatic execution
- No Jupyter notebooks, no web UI in v1

## What's built

| Tool | Status | What it does |
|------|--------|--------------|
| `ingest.py` | Done | Load CSV, Excel, Stata, SPSS → DataFrame |
| `profile.py` | Done | Shape, dtypes, nulls, summary stats → pydantic model |
| `export.py` | Done | Profile table + per-column distribution plots as PNG |
| `merge.py` | Planned | Merge operations (approval gate required) |
| `analysis.py` | Planned | Run analysis (approval gate required) |
| `agent.py` | Planned | Main loop wiring tools together |
| `r_bridge.py` | Planned | R execution via subprocess (after Python stack complete) |

## Roadmap

- v1: CLI, Christian operates on researcher's behalf
- v2+: Stata `.do` file generation, session memory, potential Cowork delivery
