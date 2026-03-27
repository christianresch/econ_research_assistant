# Backlog

## Done
- [x] ingest.py — load_dataset(path) → DataFrame
        handles CSV, Excel, Stata (.dta), SPSS (.sav)
        raises ValueError for unsupported formats
        tests + fixtures for all four formats
- [x] profile.py — profile_dataset(df) → ProfileReport
        shape, column names, dtypes
        null counts per column
        summary statistics for numeric columns
        output as structured pydantic model, not print statements
- [x] export.py — export_profile_table, export_distributions
        profile table as PNG via matplotlib table rendering
        per-column distribution plots (histplot+KDE / barh)
        skips columns with > 50% missing
        timestamped filenames: {name}_profile_{ts}.png / {name}_{col}_{ts}.png

## In progress

## Later — break down when we get here
- [ ] merge.py (approval gate required)
- [ ] analysis.py (approval gate required)
- [ ] agent.py — main loop wiring tools together
- [ ] r_bridge.py (after Python stack working end-to-end)

## Icebox — v2 and beyond
- [ ] Stata .do file generation
- [ ] Web UI or Cowork delivery for partner
- [ ] Session memory / past analysis retrieval
