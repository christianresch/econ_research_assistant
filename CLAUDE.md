# Econ Data Analysis Assistant — CLAUDE.md

## What this is
A Python CLI tool that helps an economics researcher explore, 
merge, and analyze datasets. The agent proposes plans and waits 
for explicit human approval before merging data or running 
analysis. You (Christian) operate it; the researcher reviews 
outputs.

## Stack
- Python 3.11+, async/await throughout
- anthropic SDK — raw Messages API with tool use, no framework
- pandas for data loading and manipulation
- pyreadstat for Stata (.dta) and SPSS (.sav) ingestion
- matplotlib + seaborn for charts
- rpy2 or subprocess for R script execution (R must be installed)
- pydantic for all internal data models
- pytest for tests
- python-dotenv for env management

## Project layout
src/
  agent.py          # main loop: ingests question, runs tool use
  tools/
    ingest.py       # load CSV, Excel, Stata, SPSS → DataFrame
    profile.py      # data exploration: shape, dtypes, nulls, stats
    merge.py        # merge operations (only after approval)
    analysis.py     # run analysis (only after approval)
    export.py       # save charts and tables to outputs/
    r_bridge.py     # write + execute R scripts via subprocess
  prompts/
    system.md       # runtime agent instructions
    analysis_plan_template.md  # approval gate template
data/               # input datasets (never modified by agent)
outputs/            # all agent-generated files go here
tests/
CLAUDE.md
.env                # ANTHROPIC_API_KEY

## Hard rules
- Never modify anything in data/ — treat it as read-only
- Never execute merge or analysis without logging the approval
- All outputs go to outputs/ with timestamped filenames
- No hardcoded paths or API keys
- Type hints everywhere
- One tool per file in src/tools/

## Approval gates
The agent MUST stop and present a written plan before:
1. Any merge operation
2. Any analysis execution
These are non-negotiable checkpoints. The plan format lives in
src/prompts/analysis_plan_template.md.

## Task discipline for Claude Code sessions
- One task per session, scoped tightly
- /clear between tasks
- Build tools in this order: ingest → profile → export → merge → analysis → r_bridge
- Don't build r_bridge until merge and analysis work in Python

## Session startup
At the start of every session, read BACKLOG.md and DECISIONS.md before doing anything. The current task is whatever is marked "In progress" in BACKLOG.md.

## What NOT to do
- No Jupyter notebooks
- No LangChain, LlamaIndex, or agent frameworks
- No Stata execution (write .do files only)
- Don't add dependencies without updating requirements.txt
