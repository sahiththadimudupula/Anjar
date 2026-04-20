from __future__ import annotations

import pandas as pd

from core.formatting import coerce_numeric_columns
from calculations.helper_sheet_engine import apply_helper_write_back


NUMERIC_EDITABLE_COLUMNS = [
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
]


def recalculate_working_state(
    working_master_dataframe: pd.DataFrame,
    helper_dataframes: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    recalculated_dataframe = working_master_dataframe.copy()
    recalculated_dataframe = coerce_numeric_columns(recalculated_dataframe, NUMERIC_EDITABLE_COLUMNS)

    recalculated_dataframe, helper_dataframes = apply_helper_write_back(
        recalculated_dataframe,
        helper_dataframes,
    )

    return recalculated_dataframe, helper_dataframes
