"""validator.py

Module that contains lots of validating functions
"""
from typing import List
import numpy as np
import pandas as pd

EXPECTED_VARS = {
    'timestamp': np.int64,
    'lon': np.float64,
    'lat': np.float64,
    'depth': np.float64,
}


def header_check(df: pd.DataFrame) -> List[str]:
    """Validates csv columns"""
    expected_columns = list(EXPECTED_VARS.keys())
    missing_cols = []
    for col in expected_columns:
        if col not in df.columns:
            missing_cols.append(col)
    return missing_cols


def dtype_check(df: pd.DataFrame) -> List[str]:
    """Validates the csv data types"""
    incorrect_dtypes = []
    for key, col in df.items():
        if col.dtype != EXPECTED_VARS[key]:
            incorrect_dtypes.append(key)
    return incorrect_dtypes
