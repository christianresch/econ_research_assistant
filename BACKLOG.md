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

## In progress
- [ ] export.py — Implement src/tools/export.py for data exploration output.

It should expose two functions:

1. export_profile_table(report: ProfileReport, name: str) -> Path
   Saves a summary table as a PNG to outputs/.
   Table rows = one per column. Columns:
   - column name, dtype, % missing, n_unique
   - for numeric: mean, std, min, median, max
   - for categorical: top 3 values with counts
   Use matplotlib's table rendering, not seaborn.
   Filename: {name}_profile_{timestamp}.png

2. export_distributions(df: pd.DataFrame, 
                         report: ProfileReport, 
                         name: str) -> list[Path]
   Saves one plot per column to outputs/.
   - numeric columns: histogram with a KDE line (seaborn)
   - categorical columns: horizontal bar chart of top 10 values
   - skip columns with > 50% missing
   Filename: {name}_{column_name}_{timestamp}.png
   Returns list of all paths written.

Import ProfileReport from src/tools/profile.py.
Timestamp format: %Y%m%d_%H%M%S
outputs/ directory should be created if it doesn't exist.
Write tests in tests/test_export.py using a small synthetic 
ProfileReport and DataFrame — no real data needed.
Run tests when done.

## Later — break down when we get here
- [ ] merge.py (approval gate required)
- [ ] analysis.py (approval gate required)
- [ ] agent.py — main loop wiring tools together
- [ ] r_bridge.py (after Python stack working end-to-end)

## Icebox — v2 and beyond
- [ ] Stata .do file generation
- [ ] Web UI or Cowork delivery for partner
- [ ] Session memory / past analysis retrieval
