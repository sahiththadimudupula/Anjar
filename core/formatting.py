from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

import pandas as pd

from config.constants import DEFAULT_DECIMAL_PLACES


def excel_round(value: float | int | None, digits: int = DEFAULT_DECIMAL_PLACES) -> float | None:
    if value is None or pd.isna(value):
        return None
    quantizer = Decimal("1") if digits == 0 else Decimal(f"1.{'0' * digits}")
    return float(Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP))


def format_number(value: object, digits: int = DEFAULT_DECIMAL_PLACES) -> object:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, (int, float)):
        return f"{value:,.{digits}f}"
    return value


def build_formatted_display_dataframe(
    dataframe: pd.DataFrame,
    numeric_columns: Iterable[str],
    digits: int = DEFAULT_DECIMAL_PLACES,
) -> pd.DataFrame:
    display_dataframe = dataframe.copy()
    for column_name in numeric_columns:
        if column_name in display_dataframe.columns:
            display_dataframe[column_name] = display_dataframe[column_name].apply(
                lambda value: format_number(value, digits)
            )
    return display_dataframe


def coerce_numeric_columns(dataframe: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    cleaned_dataframe = dataframe.copy()
    for column_name in column_names:
        if column_name in cleaned_dataframe.columns:
            cleaned_dataframe[column_name] = pd.to_numeric(cleaned_dataframe[column_name], errors="coerce")
    return cleaned_dataframe
