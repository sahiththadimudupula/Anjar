from __future__ import annotations

from pathlib import Path
from shutil import copyfileobj

import pandas as pd
import streamlit as st

from config.constants import CUT_SEW_TABLE_HEIGHT
from core.cut_sew_workbook import (
    cut_sew_workbook_exists,
    load_cut_sew_tables,
    resolve_cut_sew_workbook_path,
    update_input_values_and_recalculate,
)
from core.formatting import build_formatted_display_dataframe
from ui.table_renderer import render_html_table


INPUT_FLAG_COLUMN = "Formula"
INPUT_VALUE_COLUMN = "Value"


def _detect_numeric_columns(dataframe: pd.DataFrame) -> list[str]:
    numeric_columns: list[str] = []
    for column_name in dataframe.columns:
        numeric_series = pd.to_numeric(dataframe[column_name], errors="coerce")
        if numeric_series.notna().any():
            numeric_columns.append(column_name)
    return numeric_columns


def _save_uploaded_cut_sew_workbook(uploaded_file) -> Path:
    workbook_path = resolve_cut_sew_workbook_path()
    workbook_path.parent.mkdir(parents=True, exist_ok=True)

    uploaded_file.seek(0)
    with open(workbook_path, "wb") as target_file:
        copyfileobj(uploaded_file, target_file)

    return workbook_path


def _render_upload_button_only() -> None:
    uploaded_file = st.file_uploader(
        "Upload updated Cut & Sew Excel file",
        type=["xlsx"],
        key="cut_sew_workbook_uploader",
        label_visibility="collapsed",
        help="Upload a new Cut & Sew workbook. It will replace input/Anjar_TT_cut&sew.xlsx used by this tab.",
    )

    if uploaded_file is None:
        return

    _, action_column, _ = st.columns([3.5, 1.3, 3.5])
    with action_column:
        if st.button("Update File", key="update_cut_sew_workbook", width="stretch"):
            _save_uploaded_cut_sew_workbook(uploaded_file)
            st.success("Cut & Sew workbook updated.")
            st.rerun()


def _has_input_rows(dataframe: pd.DataFrame) -> bool:
    if INPUT_FLAG_COLUMN not in dataframe.columns or INPUT_VALUE_COLUMN not in dataframe.columns:
        return False

    input_mask = dataframe[INPUT_FLAG_COLUMN].astype(str).str.strip().str.lower().eq("input")
    return bool(input_mask.any())


def _build_input_editor_dataframe(values_dataframe: pd.DataFrame, formulas_dataframe: pd.DataFrame) -> pd.DataFrame:
    input_mask = formulas_dataframe[INPUT_FLAG_COLUMN].astype(str).str.strip().str.lower().eq("input")
    editor_dataframe = values_dataframe.loc[input_mask].copy()

    display_columns = [
        column_name
        for column_name in editor_dataframe.columns
        if not str(column_name).startswith("__")
    ]

    preferred_columns = [
        column_name
        for column_name in ["Month", "Section", "Metric", "Category", INPUT_VALUE_COLUMN]
        if column_name in display_columns
    ]

    remaining_columns = [
        column_name
        for column_name in display_columns
        if column_name not in preferred_columns and column_name != INPUT_FLAG_COLUMN
    ]

    selected_columns = preferred_columns + remaining_columns[:3]
    selected_columns = ["__excel_row_number"] + selected_columns

    return editor_dataframe[selected_columns].set_index("__excel_row_number", drop=True)


def _normalize_editor_values(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.replace(",", "", regex=False).str.strip()


def _extract_changed_values(original_editor: pd.DataFrame, edited_editor: pd.DataFrame) -> dict[int, object]:
    original_values = _normalize_editor_values(original_editor[INPUT_VALUE_COLUMN])
    edited_values = _normalize_editor_values(edited_editor[INPUT_VALUE_COLUMN])

    changed_updates: dict[int, object] = {}
    for excel_row_number, edited_value in edited_values.items():
        original_value = original_values.loc[excel_row_number]
        if edited_value != original_value:
            changed_updates[int(excel_row_number)] = edited_editor.loc[excel_row_number, INPUT_VALUE_COLUMN]

    return changed_updates


def _render_input_editor(
    workbook_path: Path,
    sheet_name: str,
    values_dataframe: pd.DataFrame,
    formulas_dataframe: pd.DataFrame,
    metadata: dict[str, object],
) -> None:
    if not _has_input_rows(formulas_dataframe):
        return

    with st.expander(f"Edit input values for {sheet_name}", expanded=False):
        st.caption("Only rows marked as input are editable. Formula cells are protected.")

        editor_dataframe = _build_input_editor_dataframe(values_dataframe, formulas_dataframe)
        if editor_dataframe.empty:
            st.info("No editable input rows found.")
            return

        disabled_columns = [column for column in editor_dataframe.columns if column != INPUT_VALUE_COLUMN]
        edited_dataframe = st.data_editor(
            editor_dataframe,
            width="stretch",
            hide_index=True,
            disabled=disabled_columns,
            column_config={
                INPUT_VALUE_COLUMN: st.column_config.NumberColumn(
                    label=INPUT_VALUE_COLUMN,
                    format="%.2f",
                    step=0.01,
                )
            },
            key=f"cut_sew_input_editor_{sheet_name}",
        )

        changed_updates = _extract_changed_values(editor_dataframe, edited_dataframe)
        _, button_column, _ = st.columns([3.3, 1.4, 3.3])
        with button_column:
            if st.button(
                "Apply & Recalculate",
                key=f"cut_sew_apply_inputs_{sheet_name}",
                width="stretch",
                disabled=not bool(changed_updates),
            ):
                try:
                    result = update_input_values_and_recalculate(
                        workbook_path=workbook_path,
                        sheet_name=sheet_name,
                        header_excel_row=int(metadata["header_excel_row"]),
                        row_value_updates=changed_updates,
                    )
                except Exception as exc:
                    st.error(str(exc))
                    return

                if result["recalculated"]:
                    st.success(f"Updated {result['updated_count']} input value(s) and recalculated Excel links.")
                else:
                    st.warning(
                        f"Updated {result['updated_count']} input value(s), but automatic Excel recalculation did not complete. "
                        f"{result['message']}"
                    )
                st.rerun()


def _render_table(title: str, dataframe: pd.DataFrame, *, mode_label: str) -> None:
    st.markdown(
        f'<div class="section-strip">{title} - {mode_label} &nbsp;&nbsp;|&nbsp;&nbsp; Rows: {len(dataframe):,.0f} | Columns: {len(dataframe.columns):,.0f}</div>',
        unsafe_allow_html=True,
    )

    numeric_columns = _detect_numeric_columns(dataframe)
    display_dataframe = build_formatted_display_dataframe(dataframe, numeric_columns=numeric_columns)
    is_compact_table = len(display_dataframe.columns) <= 10
    render_html_table(
        display_dataframe,
        height=CUT_SEW_TABLE_HEIGHT,
        compact=is_compact_table,
    )


def _render_sheet(
    workbook_path: Path,
    sheet_name: str,
    values_dataframe: pd.DataFrame | None,
    formulas_dataframe: pd.DataFrame | None,
    metadata: dict[str, object],
) -> None:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)

    if values_dataframe is not None:
        clean_values_dataframe = values_dataframe[
            [column for column in values_dataframe.columns if not str(column).startswith("__")]
        ].copy()
        _render_table(sheet_name, clean_values_dataframe, mode_label="Values")

    if values_dataframe is not None and formulas_dataframe is not None:
        _render_input_editor(
            workbook_path,
            sheet_name,
            values_dataframe,
            formulas_dataframe,
            metadata,
        )

    if formulas_dataframe is not None:
        with st.expander(f"Show formulas for {sheet_name}", expanded=False):
            clean_formulas_dataframe = formulas_dataframe[
                [column for column in formulas_dataframe.columns if not str(column).startswith("__")]
            ].copy()
            _render_table(sheet_name, clean_formulas_dataframe, mode_label="Formulas")

    st.markdown("</div>", unsafe_allow_html=True)


def _table_map(tables: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(table["sheet_name"]): table for table in tables}


def render_cut_sew_tab() -> None:
    _render_upload_button_only()

    workbook_path = resolve_cut_sew_workbook_path()
    if not cut_sew_workbook_exists(workbook_path):
        st.error(f"Cut & Sew workbook not found at: {workbook_path}")
        return

    try:
        value_tables = load_cut_sew_tables(workbook_path, data_only=True)
        formula_tables = load_cut_sew_tables(workbook_path, data_only=False)
    except Exception as exc:
        st.error(f"Unable to read Cut & Sew workbook. Please upload a valid .xlsx file. Error: {exc}")
        return

    if not value_tables and not formula_tables:
        st.info("No tables found in the Cut & Sew workbook.")
        return

    value_table_map = _table_map(value_tables)
    formula_table_map = _table_map(formula_tables)
    sheet_names = list(dict.fromkeys(list(value_table_map.keys()) + list(formula_table_map.keys())))

    for sheet_name in sheet_names:
        value_table = value_table_map.get(sheet_name)
        formula_table = formula_table_map.get(sheet_name)

        values_dataframe = value_table["dataframe"] if value_table else None
        formulas_dataframe = formula_table["dataframe"] if formula_table else None
        metadata = formula_table["metadata"] if formula_table else value_table["metadata"]

        _render_sheet(
            workbook_path,
            sheet_name,
            values_dataframe,
            formulas_dataframe,
            metadata,
        )
