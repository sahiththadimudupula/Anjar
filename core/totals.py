from __future__ import annotations

import pandas as pd

from config.constants import TOTAL_LABEL
from core.dataframe_utils import parse_machine_count


def _sum_numeric_series(series: pd.Series) -> float | None:
    numeric_series = pd.to_numeric(series, errors="coerce")
    if numeric_series.notna().any():
        return float(numeric_series.sum())
    return None


def append_total_row(dataframe: pd.DataFrame, label_column: str | None = None) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe.copy()

    total_row: dict[str, object] = {column_name: "" for column_name in dataframe.columns}

    if label_column and label_column in dataframe.columns:
        total_row[label_column] = TOTAL_LABEL
    elif "Section" in dataframe.columns:
        total_row["Section"] = TOTAL_LABEL

    if "Machine_Count" in dataframe.columns:
        machine_total = dataframe["Machine_Count"].apply(parse_machine_count).dropna().sum()
        total_row["Machine_Count"] = float(machine_total) if not pd.isna(machine_total) else None

    for column_name in dataframe.columns:
        if column_name == "Machine_Count":
            continue
        summed_value = _sum_numeric_series(dataframe[column_name])
        if summed_value is not None:
            total_row[column_name] = summed_value

    if "__row_key" in dataframe.columns:
        total_row["__row_key"] = "__total__"
    if "__excel_row_number" in dataframe.columns:
        total_row["__excel_row_number"] = None
    if "__row_order" in dataframe.columns:
        total_row["__row_order"] = float("inf")

    total_dataframe = pd.DataFrame([total_row], columns=dataframe.columns)
    return pd.concat([dataframe, total_dataframe], ignore_index=True)


def build_tab_kpis(dataframe: pd.DataFrame) -> list[dict[str, str]]:
    parsed_machine_count_total = dataframe["Machine_Count"].apply(parse_machine_count).dropna().sum() if "Machine_Count" in dataframe.columns else 0.0
    total_final_manpower = pd.to_numeric(dataframe.get("BE_Final_Manpower"), errors="coerce").sum()
    total_sections = dataframe["Section"].astype(str).replace("nan", pd.NA).dropna().nunique() if "Section" in dataframe.columns else 0

    return [
        {"label": "Total Sections Parsed", "value": f"{total_sections:,.0f}"},
        {"label": "Machine Count", "value": f"{parsed_machine_count_total:,.2f}"},
        {"label": "Total Final Manpower", "value": f"{total_final_manpower:,.2f}"},
    ]
