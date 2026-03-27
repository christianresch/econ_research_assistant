from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.tools.profile import ProfileReport

_DEFAULT_OUTPUT_DIR = Path("outputs")


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_profile_table(
    report: ProfileReport,
    name: str,
    output_dir: Path = _DEFAULT_OUTPUT_DIR,
) -> Path:
    """Save a summary of ProfileReport as a PNG table to output_dir.

    Each row corresponds to one column. Columns shown:
    - Column name, dtype, % missing, n_unique
    - Numeric columns: mean, std, min, median, max
    - Categorical columns: top 3 values with counts

    Args:
        report: The profile to render.
        name: Short label used in the filename.
        output_dir: Directory to write to. Created if it does not exist.

    Returns:
        Path of the saved .png file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    headers = ["Column", "Dtype", "Missing%", "Unique", "Summary"]
    rows = []
    for c in report.columns:
        if c.mean is not None:
            summary = (
                f"mean={c.mean}  std={c.std}  "
                f"min={c.min}  median={c.median}  max={c.max}"
            )
        else:
            top3 = list((c.top_values or {}).items())[:3]
            summary = "  ".join(f"{k}({v})" for k, v in top3)
        rows.append([c.name, c.dtype, f"{c.pct_missing}%", str(c.n_unique), summary])

    n_rows = len(rows)
    fig_height = max(2.0, 0.4 * (n_rows + 2))
    fig, ax = plt.subplots(figsize=(16, fig_height))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=headers,
        cellLoc="left",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.auto_set_column_width(col=list(range(len(headers))))

    ts = _timestamp()
    path = output_dir / f"{name}_profile_{ts}.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return path


def export_distributions(
    df: pd.DataFrame,
    report: ProfileReport,
    name: str,
    output_dir: Path = _DEFAULT_OUTPUT_DIR,
) -> list[Path]:
    """Save one distribution plot per column to output_dir.

    Numeric columns: histogram with KDE line (seaborn).
    Categorical columns: horizontal bar chart of top 10 values.
    Columns with > 50% missing values are skipped.

    Args:
        df: The source DataFrame (used for raw values).
        report: The profile describing the DataFrame's columns.
        name: Short label used in filenames.
        output_dir: Directory to write to. Created if it does not exist.

    Returns:
        List of paths for all files written (one per non-skipped column).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = _timestamp()
    paths: list[Path] = []

    for col in report.columns:
        if col.pct_missing > 50.0:
            continue

        series = df[col.name].dropna()
        fig, ax = plt.subplots(figsize=(8, 4))

        if col.mean is not None:
            sns.histplot(series, kde=True, ax=ax)
            ax.set_title(f"{col.name} — distribution")
            ax.set_xlabel(col.name)
        else:
            counts = series.value_counts().head(10)
            counts.sort_values().plot(kind="barh", ax=ax)
            ax.set_title(f"{col.name} — top values")
            ax.set_xlabel("count")

        path = output_dir / f"{name}_{col.name}_{ts}.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        paths.append(path)

    return paths
