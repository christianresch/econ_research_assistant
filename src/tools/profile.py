import pandas as pd
from pydantic import BaseModel


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    n_missing: int
    pct_missing: float
    n_unique: int
    # numeric stats (None for non-numeric columns)
    mean: float | None = None
    std: float | None = None
    min: float | None = None
    p25: float | None = None
    median: float | None = None
    p75: float | None = None
    max: float | None = None
    # categorical stats (None for numeric columns)
    top_values: dict[str, int] | None = None


class DatasetProfile(BaseModel):
    n_rows: int
    n_cols: int
    n_complete_rows: int
    pct_complete_rows: float
    columns: list[ColumnProfile]


def profile_dataset(df: pd.DataFrame) -> DatasetProfile:
    """Profile a DataFrame: shape, missingness, descriptive statistics.

    Args:
        df: The DataFrame to profile.

    Returns:
        A DatasetProfile with row/column counts and per-column statistics.
    """
    n_rows, n_cols = df.shape
    n_complete = int(df.dropna().shape[0])
    pct_complete = round(n_complete / n_rows * 100, 2) if n_rows > 0 else 0.0

    columns: list[ColumnProfile] = []
    for col in df.columns:
        series = df[col]
        n_missing = int(series.isna().sum())
        pct_missing = round(n_missing / n_rows * 100, 2) if n_rows > 0 else 0.0
        n_unique = int(series.nunique(dropna=False))

        if pd.api.types.is_numeric_dtype(series):
            desc = series.describe(percentiles=[0.25, 0.5, 0.75])
            columns.append(ColumnProfile(
                name=col,
                dtype=str(series.dtype),
                n_missing=n_missing,
                pct_missing=pct_missing,
                n_unique=n_unique,
                mean=round(float(desc["mean"]), 4),
                std=round(float(desc["std"]), 4),
                min=round(float(desc["min"]), 4),
                p25=round(float(desc["25%"]), 4),
                median=round(float(desc["50%"]), 4),
                p75=round(float(desc["75%"]), 4),
                max=round(float(desc["max"]), 4),
            ))
        else:
            top = (
                series.dropna()
                .value_counts()
                .head(5)
                .to_dict()
            )
            top_str = {str(k): int(v) for k, v in top.items()}
            columns.append(ColumnProfile(
                name=col,
                dtype=str(series.dtype),
                n_missing=n_missing,
                pct_missing=pct_missing,
                n_unique=n_unique,
                top_values=top_str,
            ))

    return DatasetProfile(
        n_rows=n_rows,
        n_cols=n_cols,
        n_complete_rows=n_complete,
        pct_complete_rows=pct_complete,
        columns=columns,
    )


def format_profile(profile: DatasetProfile) -> str:
    """Render a DatasetProfile as a human-readable string.

    Args:
        profile: The profile to render.

    Returns:
        A formatted multi-line string suitable for display or logging.
    """
    lines: list[str] = [
        f"Rows: {profile.n_rows:,}  |  Columns: {profile.n_cols}",
        f"Complete rows (no missing values): {profile.n_complete_rows:,} "
        f"({profile.pct_complete_rows}%)",
        "",
        f"{'Column':<30} {'Dtype':<12} {'Missing':>8} {'Missing%':>9} "
        f"{'Unique':>7}  Summary",
        "-" * 90,
    ]

    for c in profile.columns:
        if c.mean is not None:
            summary = (
                f"mean={c.mean}  std={c.std}  "
                f"[{c.min}, {c.p25}, {c.median}, {c.p75}, {c.max}]"
            )
        else:
            top = ", ".join(f"{k}({v})" for k, v in (c.top_values or {}).items())
            summary = f"top: {top}"

        lines.append(
            f"{c.name:<30} {c.dtype:<12} {c.n_missing:>8} {c.pct_missing:>8}%"
            f" {c.n_unique:>7}  {summary}"
        )

    return "\n".join(lines)
