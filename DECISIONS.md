# Decisions

## Core principles

### Human control is structural, not behavioral
The system must make safe behavior the path of least resistance,
not the path of most discipline. This applies at every level:

- The agent cannot merge or analyze without explicit confirmation
- Claude Code cannot land code to main without a diff review
- Process controls are encoded into workflow, not relied on as habits

This principle governs all future design decisions in this project.

---

## 2026-03-27

### Stack
- Python 3.11+ with conda environment
- Raw Anthropic Messages API with tool use — no agent framework
- pandas for data manipulation
- pyreadstat for Stata (.dta) and SPSS (.sav)
- matplotlib + seaborn for charts and tables
- subprocess for R execution (not rpy2 — simpler install,
  sufficient feedback loop for our needs)
- pydantic for internal data models
- pytest for tests

### Scope boundaries for v1
- Stata: write .do files only, no programmatic execution
- No Jupyter notebooks — keep outputs as files only
- No web UI in v1 — Christian operates, researcher reviews outputs
- Charts + tables saved to outputs/ with timestamped filenames

### Architecture
- Approval gates hardcoded before merge and analysis — not
  configurable, not skippable
- Approvals logged to logs/approvals.jsonl for audit trail
- data/ directory is read-only — agent never modifies inputs
- All generated files go to outputs/

### Interface
- CLI for v1, Christian operates on partner's behalf
- Cowork as potential future delivery mechanism once agent
  loop is proven
