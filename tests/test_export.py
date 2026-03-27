import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for tests
import pandas as pd
import pytest

from src.tools.profile import profile_dataset
from src.tools.export import export_profile_table, export_distributions

TIMESTAMP_RE = re.compile(r"\d{8}_\d{6}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mixed_df() -> pd.DataFrame:
    return pd.DataFrame({
        "age":    [25, 30, 35, 40, 45],
        "income": [50_000.0, 60_000.0, 75_000.0, None, 120_000.0],
        "country": ["US", "UK", "US", "DE", "US"],
        "status":  ["active", "inactive", "active", "active", None],
    })


@pytest.fixture
def mixed_report(mixed_df):
    return profile_dataset(mixed_df)


@pytest.fixture
def mostly_missing_df() -> pd.DataFrame:
    # "sparse" column has 80% missing — should be skipped by export_distributions
    return pd.DataFrame({
        "x":      [1.0, 2.0, 3.0, 4.0, 5.0],
        "sparse": [None, None, None, None, 1.0],
    })


# ---------------------------------------------------------------------------
# export_profile_table
# ---------------------------------------------------------------------------

def test_profile_table_creates_file(mixed_report, tmp_path):
    path = export_profile_table(mixed_report, "test", output_dir=tmp_path)
    assert path.exists()


def test_profile_table_is_png(mixed_report, tmp_path):
    path = export_profile_table(mixed_report, "test", output_dir=tmp_path)
    assert path.suffix == ".png"


def test_profile_table_filename_format(mixed_report, tmp_path):
    path = export_profile_table(mixed_report, "survey", output_dir=tmp_path)
    assert path.name.startswith("survey_profile_")
    assert TIMESTAMP_RE.search(path.name)


def test_profile_table_creates_output_dir(mixed_report, tmp_path):
    subdir = tmp_path / "new_dir"
    assert not subdir.exists()
    export_profile_table(mixed_report, "t", output_dir=subdir)
    assert subdir.exists()


def test_profile_table_returns_correct_parent(mixed_report, tmp_path):
    path = export_profile_table(mixed_report, "t", output_dir=tmp_path)
    assert path.parent == tmp_path


# ---------------------------------------------------------------------------
# export_distributions — file creation
# ---------------------------------------------------------------------------

def test_distributions_creates_files(mixed_df, mixed_report, tmp_path):
    paths = export_distributions(mixed_df, mixed_report, "test", output_dir=tmp_path)
    assert len(paths) > 0
    for p in paths:
        assert p.exists()


def test_distributions_all_png(mixed_df, mixed_report, tmp_path):
    paths = export_distributions(mixed_df, mixed_report, "test", output_dir=tmp_path)
    for p in paths:
        assert p.suffix == ".png"


def test_distributions_filename_format(mixed_df, mixed_report, tmp_path):
    paths = export_distributions(mixed_df, mixed_report, "survey", output_dir=tmp_path)
    for p in paths:
        assert p.name.startswith("survey_")
        assert TIMESTAMP_RE.search(p.name)


def test_distributions_one_file_per_non_skipped_column(mixed_df, mixed_report, tmp_path):
    # mixed_df has 4 columns, none with > 50% missing
    paths = export_distributions(mixed_df, mixed_report, "t", output_dir=tmp_path)
    assert len(paths) == 4


def test_distributions_skips_mostly_missing(mostly_missing_df, tmp_path):
    report = profile_dataset(mostly_missing_df)
    paths = export_distributions(mostly_missing_df, report, "t", output_dir=tmp_path)
    # "sparse" has 80% missing and should be skipped; only "x" written
    assert len(paths) == 1
    assert "x" in paths[0].name


def test_distributions_creates_output_dir(mixed_df, mixed_report, tmp_path):
    subdir = tmp_path / "plots"
    assert not subdir.exists()
    export_distributions(mixed_df, mixed_report, "t", output_dir=subdir)
    assert subdir.exists()


def test_distributions_column_names_in_filenames(mixed_df, mixed_report, tmp_path):
    paths = export_distributions(mixed_df, mixed_report, "survey", output_dir=tmp_path)
    written_names = {p.name for p in paths}
    for col in mixed_df.columns:
        assert any(col in n for n in written_names)
