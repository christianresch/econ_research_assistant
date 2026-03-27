import pytest
import pandas as pd
from pathlib import Path
from src.tools.ingest import load_dataset

FIXTURES = Path(__file__).parent / "fixtures"

EXPECTED_COLUMNS = {"id", "value", "label"}
EXPECTED_ROWS = 3


def _assert_basic_shape(df: pd.DataFrame) -> None:
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == EXPECTED_COLUMNS
    assert len(df) == EXPECTED_ROWS


def test_load_csv():
    df = load_dataset(str(FIXTURES / "sample.csv"))
    _assert_basic_shape(df)


def test_load_xlsx():
    df = load_dataset(str(FIXTURES / "sample.xlsx"))
    _assert_basic_shape(df)


def test_load_dta():
    df = load_dataset(str(FIXTURES / "sample.dta"))
    _assert_basic_shape(df)


def test_load_sav():
    df = load_dataset(str(FIXTURES / "sample.sav"))
    _assert_basic_shape(df)


def test_unsupported_format_raises():
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_dataset("data/something.parquet")


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_dataset("data/nonexistent.csv")
