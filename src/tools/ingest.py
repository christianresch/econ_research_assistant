import pandas as pd
import pyreadstat
from pathlib import Path


def load_dataset(path: str) -> pd.DataFrame:
    """Load a dataset from CSV, Excel, Stata, or SPSS into a DataFrame.

    Args:
        path: Path to the dataset file.

    Returns:
        A pandas DataFrame with the loaded data.

    Raises:
        ValueError: If the file extension is not supported.
        FileNotFoundError: If the file does not exist.
    """
    p = Path(path)

    ext = p.suffix.lower()

    if ext not in (".csv", ".xlsx", ".xls", ".dta", ".sav"):
        raise ValueError(
            f"Unsupported file format: '{ext}'. "
            "Supported formats: .csv, .xlsx, .xls, .dta, .sav"
        )

    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    elif ext == ".dta":
        df, _ = pyreadstat.read_dta(path)
        return df
    else:  # .sav
        df, _ = pyreadstat.read_sav(path)
        return df
