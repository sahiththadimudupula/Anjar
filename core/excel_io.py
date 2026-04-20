from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from config.constants import INPUT_WORKBOOK_PATH
from core.dataframe_utils import create_row_metadata, normalize_column_names


def resolve_workbook_path(workbook_path: str | None = None) -> Path:
    selected_path = workbook_path or INPUT_WORKBOOK_PATH
    return Path(selected_path)


def workbook_exists(workbook_path: str | None = None) -> bool:
    return resolve_workbook_path(workbook_path).exists()


def load_sheet_dataframe(workbook_path: str, sheet_name: str) -> pd.DataFrame:
    sheet_dataframe = pd.read_excel(workbook_path, sheet_name=sheet_name)
    sheet_dataframe = normalize_column_names(sheet_dataframe)
    return sheet_dataframe


def load_master_dataframe(workbook_path: str, sheet_name: str) -> pd.DataFrame:
    master_dataframe = load_sheet_dataframe(workbook_path, sheet_name)
    return create_row_metadata(master_dataframe)


def load_workbook_sheet_names(workbook_path: str) -> list[str]:
    workbook = load_workbook(workbook_path, read_only=True, data_only=False)
    try:
        return workbook.sheetnames
    finally:
        workbook.close()


def load_helper_dataframes(workbook_path: str, helper_sheet_names: list[str]) -> dict[str, pd.DataFrame]:
    helper_dataframes: dict[str, pd.DataFrame] = {}
    for helper_sheet_name in helper_sheet_names:
        helper_dataframes[helper_sheet_name] = load_sheet_dataframe(workbook_path, helper_sheet_name)
    return helper_dataframes
