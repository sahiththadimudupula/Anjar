from __future__ import annotations

import pandas as pd
import streamlit as st

from calculations.recalculate_engine import recalculate_working_state
from config.constants import COMPACT_TABLE_HEIGHT, DATA_EDITOR_HEIGHT, EDITABLE_COLUMNS, VISIBLE_COMPACT_COLUMNS
from core.formatting import build_formatted_display_dataframe
from core.totals import append_total_row
from core.write_back import update_working_dataframe_from_editor
from ui.table_renderer import render_html_table

NUMERIC_EDITOR_COLUMNS = [
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
]


def _build_editor_config(section_dataframe: pd.DataFrame):
    editor_config = {}

    for column_name in section_dataframe.columns:
        if column_name in NUMERIC_EDITOR_COLUMNS:
            editor_config[column_name] = st.column_config.NumberColumn(
                label=column_name,
                format="%.2f",
                step=0.01,
            )
        elif column_name == "Remarks":
            editor_config[column_name] = st.column_config.TextColumn(label=column_name, width="medium")

    return editor_config


def _normalize_comparable_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    comparable_dataframe = dataframe.copy()
    for column_name in comparable_dataframe.columns:
        if column_name in NUMERIC_EDITOR_COLUMNS:
            comparable_dataframe[column_name] = pd.to_numeric(comparable_dataframe[column_name], errors="coerce").round(2)
        else:
            comparable_dataframe[column_name] = comparable_dataframe[column_name].fillna("").astype(str)
    return comparable_dataframe


def _has_editor_changes(original_dataframe: pd.DataFrame, edited_dataframe: pd.DataFrame) -> bool:
    original_subset = _normalize_comparable_values(original_dataframe[EDITABLE_COLUMNS])
    edited_subset = _normalize_comparable_values(edited_dataframe[EDITABLE_COLUMNS])
    return not edited_subset.equals(original_subset)


def render_section_tables(business_name: str, business_dataframe: pd.DataFrame) -> None:
    if business_dataframe.empty:
        st.info("No data is available for this business.")
        return

    for section_name, section_dataframe in business_dataframe.groupby("Section", sort=False):
        section_total = pd.to_numeric(section_dataframe["BE_Final_Manpower"], errors="coerce").sum()
        safe_section_key = f"{business_name}_{section_name}".replace(" ", "_").replace("/", "_")

        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-strip">{section_name} &nbsp;&nbsp;|&nbsp;&nbsp; Final Manpower: {section_total:,.2f}</div>',
            unsafe_allow_html=True,
        )

        compact_dataframe = section_dataframe[VISIBLE_COMPACT_COLUMNS].copy()
        compact_dataframe = append_total_row(compact_dataframe, label_column="Section")
        compact_dataframe = build_formatted_display_dataframe(compact_dataframe, numeric_columns=["BE_Final_Manpower"])
        render_html_table(compact_dataframe, height=COMPACT_TABLE_HEIGHT)

        with st.expander(f"Expand full editable table for {section_name}", expanded=False):
            editable_dataframe = section_dataframe.copy().set_index("__row_key", drop=True)
            disabled_columns = [
                column_name
                for column_name in editable_dataframe.columns
                if column_name not in EDITABLE_COLUMNS
            ]

            editor_key = f"{safe_section_key}_editor"
            button_key = f"{safe_section_key}_apply_changes"
            edited_dataframe = st.data_editor(
                editable_dataframe,
                width="stretch",
                hide_index=True,
                height=DATA_EDITOR_HEIGHT,
                disabled=disabled_columns,
                column_config=_build_editor_config(editable_dataframe),
                key=editor_key,
            )

            has_changes = _has_editor_changes(editable_dataframe, edited_dataframe)
            if has_changes:
                st.info("Changes are ready. Click Apply Section Changes to update the tab and final sheet.")

            if st.button("Apply Section Changes", key=button_key, width="stretch", disabled=not has_changes):
                updated_master_dataframe = update_working_dataframe_from_editor(
                    st.session_state.working_master_dataframe,
                    edited_dataframe,
                )
                recalculated_dataframe, helper_dataframes = recalculate_working_state(
                    updated_master_dataframe,
                    st.session_state.helper_dataframes,
                )
                st.session_state.working_master_dataframe = recalculated_dataframe
                st.session_state.helper_dataframes = helper_dataframes
                st.session_state.freeze_status = "Draft"
                st.rerun()

            expanded_total_dataframe = append_total_row(section_dataframe.copy(), label_column="Section")
            expanded_total_dataframe = expanded_total_dataframe[
                expanded_total_dataframe["Section"].astype(str) == "Total"
            ]
            expanded_total_dataframe = build_formatted_display_dataframe(
                expanded_total_dataframe,
                numeric_columns=[
                    column_name
                    for column_name in NUMERIC_EDITOR_COLUMNS
                    if column_name in expanded_total_dataframe.columns
                ],
            )
            render_html_table(expanded_total_dataframe, caption="Expanded table total")

        st.markdown("</div>", unsafe_allow_html=True)
