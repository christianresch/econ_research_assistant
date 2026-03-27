import math
import pandas as pd
import pytest
from src.tools.profile import profile_dataset, format_profile, ProfileReport, ColumnProfile


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def numeric_df() -> pd.DataFrame:
    return pd.DataFrame({
        "age": [25, 30, 35, 40, 45],
        "income": [50000.0, 60000.0, 75000.0, 90000.0, 120000.0],
    })


@pytest.fixture
def categorical_df() -> pd.DataFrame:
    return pd.DataFrame({
        "country": ["US", "UK", "US", "DE", "US"],
        "status": ["active", "inactive", "active", "active", "inactive"],
    })


@pytest.fixture
def mixed_df() -> pd.DataFrame:
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "score": [8.5, 7.0, 9.0, None, 6.5],
        "group": ["A", "B", "A", None, "B"],
    })


@pytest.fixture
def all_missing_df() -> pd.DataFrame:
    return pd.DataFrame({
        "x": [None, None, None],
        "y": [1.0, 2.0, 3.0],
    })


# ---------------------------------------------------------------------------
# ProfileReport shape
# ---------------------------------------------------------------------------

def test_row_col_counts(numeric_df):
    p = profile_dataset(numeric_df)
    assert p.n_rows == 5
    assert p.n_cols == 2


def test_column_count_matches_columns_list(mixed_df):
    p = profile_dataset(mixed_df)
    assert len(p.columns) == mixed_df.shape[1]


def test_column_names_preserved(mixed_df):
    p = profile_dataset(mixed_df)
    assert [c.name for c in p.columns] == list(mixed_df.columns)


# ---------------------------------------------------------------------------
# Complete-row statistics
# ---------------------------------------------------------------------------

def test_complete_rows_no_missing(numeric_df):
    p = profile_dataset(numeric_df)
    assert p.n_complete_rows == 5
    assert p.pct_complete_rows == 100.0


def test_complete_rows_with_missing(mixed_df):
    # only row index 3 (Diana) has missing values in both score and group
    p = profile_dataset(mixed_df)
    assert p.n_complete_rows == 4
    assert p.pct_complete_rows == 80.0


# ---------------------------------------------------------------------------
# Missing-value counts
# ---------------------------------------------------------------------------

def test_no_missing_values(numeric_df):
    p = profile_dataset(numeric_df)
    for col in p.columns:
        assert col.n_missing == 0
        assert col.pct_missing == 0.0


def test_missing_count_and_pct(mixed_df):
    p = profile_dataset(mixed_df)
    score_col = next(c for c in p.columns if c.name == "score")
    group_col = next(c for c in p.columns if c.name == "group")

    assert score_col.n_missing == 1
    assert score_col.pct_missing == 20.0

    assert group_col.n_missing == 1
    assert group_col.pct_missing == 20.0


def test_all_missing_column(all_missing_df):
    p = profile_dataset(all_missing_df)
    x_col = next(c for c in p.columns if c.name == "x")
    assert x_col.n_missing == 3
    assert x_col.pct_missing == 100.0


# ---------------------------------------------------------------------------
# Numeric column stats
# ---------------------------------------------------------------------------

def test_numeric_stats_present(numeric_df):
    p = profile_dataset(numeric_df)
    for col in p.columns:
        assert col.mean is not None
        assert col.std is not None
        assert col.min is not None
        assert col.p25 is not None
        assert col.median is not None
        assert col.p75 is not None
        assert col.max is not None


def test_numeric_stats_values(numeric_df):
    p = profile_dataset(numeric_df)
    age_col = next(c for c in p.columns if c.name == "age")

    assert age_col.mean == pytest.approx(35.0, abs=0.01)
    assert age_col.min == 25.0
    assert age_col.max == 45.0
    assert age_col.median == 35.0


def test_numeric_no_top_values(numeric_df):
    p = profile_dataset(numeric_df)
    for col in p.columns:
        assert col.top_values is None


# ---------------------------------------------------------------------------
# Categorical column stats
# ---------------------------------------------------------------------------

def test_categorical_stats_present(categorical_df):
    p = profile_dataset(categorical_df)
    for col in p.columns:
        assert col.top_values is not None
        assert col.mean is None


def test_categorical_top_values_correct(categorical_df):
    p = profile_dataset(categorical_df)
    country_col = next(c for c in p.columns if c.name == "country")

    assert country_col.top_values["US"] == 3
    assert country_col.top_values["UK"] == 1
    assert country_col.top_values["DE"] == 1


def test_categorical_top_values_capped_at_5():
    df = pd.DataFrame({"cat": [str(i) for i in range(10)]})
    p = profile_dataset(df)
    col = p.columns[0]
    assert len(col.top_values) <= 5


# ---------------------------------------------------------------------------
# Unique counts
# ---------------------------------------------------------------------------

def test_unique_counts(categorical_df):
    p = profile_dataset(categorical_df)
    country_col = next(c for c in p.columns if c.name == "country")
    assert country_col.n_unique == 3  # US, UK, DE


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_dataframe():
    df = pd.DataFrame({"a": pd.Series([], dtype=float)})
    p = profile_dataset(df)
    assert p.n_rows == 0
    assert p.pct_complete_rows == 0.0
    col = p.columns[0]
    assert col.n_missing == 0
    assert col.pct_missing == 0.0


def test_single_row():
    df = pd.DataFrame({"x": [42.0], "label": ["foo"]})
    p = profile_dataset(df)
    assert p.n_rows == 1
    assert p.n_complete_rows == 1


# ---------------------------------------------------------------------------
# format_profile
# ---------------------------------------------------------------------------

def test_format_profile_returns_string(numeric_df):
    p = profile_dataset(numeric_df)
    output = format_profile(p)
    assert isinstance(output, str)


def test_format_profile_contains_column_names(mixed_df):
    p = profile_dataset(mixed_df)
    output = format_profile(p)
    for col in mixed_df.columns:
        assert col in output


def test_format_profile_contains_row_count(numeric_df):
    p = profile_dataset(numeric_df)
    output = format_profile(p)
    assert "5" in output


def test_format_profile_contains_missing_info(mixed_df):
    p = profile_dataset(mixed_df)
    output = format_profile(p)
    # score has 1 missing value (20%)
    assert "20.0" in output
