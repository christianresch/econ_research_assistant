# Backlog

## Done
- [x] ingest.py — load_dataset(path) → DataFrame
        handles CSV, Excel, Stata (.dta), SPSS (.sav)
        raises ValueError for unsupported formats
        tests + fixtures for all four formats

## In progress
- [ ] profile.py — profile_dataset(df) → ProfileReport
        shape, column names, dtypes
        null counts per column
        summary statistics for numeric columns
        output as structured pydantic model, not print statements

- [ ] export.py — save charts and tables to outputs/
        timestamped filenames
        consistent format across all outputs

## Later — break down when we get here
- [ ] merge.py (approval gate required)
- [ ] analysis.py (approval gate required)
- [ ] agent.py — main loop wiring tools together
- [ ] r_bridge.py (after Python stack working end-to-end)

## Icebox — v2 and beyond
- [ ] Stata .do file generation
- [ ] Web UI or Cowork delivery for partner
- [ ] Session memory / past analysis retrieval
