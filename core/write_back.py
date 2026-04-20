from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from config.constants import EDITABLE_COLUMNS, MASTER_SHEET_NAME, OUTPUT_DIRECTORY


def update_working_dataframe_from_editor(
    working_master_dataframe: pd.DataFrame,
    edited_section_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    updated_dataframe = working_master_dataframe.copy()

    for row_key, edited_row in edited_section_dataframe.iterrows():
        row_selector = updated_dataframe["__row_key"] == str(row_key)
        if not row_selector.any():
            continue
        for editable_column in EDITABLE_COLUMNS:
            if editable_column in edited_row.index and editable_column in updated_dataframe.columns:
                updated_dataframe.loc[row_selector, editable_column] = edited_row[editable_column]

    return updated_dataframe.sort_values("__row_order").reset_index(drop=True)


def write_dataframe_back_to_excel(
    updated_master_dataframe: pd.DataFrame,
    workbook_path: str,
    master_sheet_name: str = MASTER_SHEET_NAME,
) -> tuple[Path, Path]:
    workbook = load_workbook(workbook_path)
    worksheet = workbook[master_sheet_name]

    header_row = 1
    header_lookup = {
        str(worksheet.cell(header_row, column_index).value).strip(): column_index
        for column_index in range(1, worksheet.max_column + 1)
        if worksheet.cell(header_row, column_index).value is not None
    }

    for _, row in updated_master_dataframe.iterrows():
        excel_row_number = int(row["__excel_row_number"])
        for editable_column in EDITABLE_COLUMNS:
            if editable_column not in header_lookup:
                continue
            cell_column = header_lookup[editable_column]
            worksheet.cell(excel_row_number, cell_column).value = row[editable_column]

    workbook.save(workbook_path)

    output_directory = Path(workbook_path).parent.parent / OUTPUT_DIRECTORY
    output_directory.mkdir(parents=True, exist_ok=True)

    timestamp_text = datetime.now().strftime("%Y%m%d_%H%M%S")
    frozen_copy_path = output_directory / f"Anjar_manning_frozen_{timestamp_text}.xlsx"
    workbook.save(frozen_copy_path)
    workbook.close()

    return Path(workbook_path), frozen_copy_path
