from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from config.constants import FINAL_TABLE_HEIGHT, HIDDEN_SYSTEM_COLUMNS
from core.formatting import build_formatted_display_dataframe
from ui.table_renderer import render_html_table
from ui.tab_cards import render_tab_cards
from core.totals import append_total_row, build_tab_kpis
from core.write_back import create_download_workbook_copy


def render_master_sheet_view(master_dataframe: pd.DataFrame, working_workbook_path: str) -> None:
    render_tab_cards(build_tab_kpis(master_dataframe))

    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Fully Updated Master Sheet</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_columns = [
        column_name
        for column_name in master_dataframe.columns
        if column_name not in HIDDEN_SYSTEM_COLUMNS and not str(column_name).startswith("__")
    ]
    display_dataframe = master_dataframe[display_columns].copy()
    display_dataframe = append_total_row(display_dataframe, label_column="Section")

    numeric_columns = [
        column_name
        for column_name in [
            "Machine_Count",
            "BE_Final_Manpower",
            "General_Shift",
            "Shift_A",
            "Shift_B",
            "Shift_C",
            "Reliever",
        ]
        if column_name in display_dataframe.columns
    ]

    display_dataframe = build_formatted_display_dataframe(display_dataframe, numeric_columns=numeric_columns)

    render_html_table(display_dataframe, height=FINAL_TABLE_HEIGHT, compact=False)

    download_workbook_path = create_download_workbook_copy(
        master_dataframe,
        working_workbook_path,
    )

    workbook_name = Path(download_workbook_path).name
    with open(download_workbook_path, "rb") as workbook_file:
        st.download_button(
            "Download Updated Workbook",
            data=workbook_file.read(),
            file_name=workbook_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="content",
        )
