from __future__ import annotations

import pandas as pd
import streamlit as st

from config.constants import FINAL_TABLE_HEIGHT, MASTER_VIEW_DEFAULT_COLUMNS
from core.formatting import build_formatted_display_dataframe


def render_master_sheet_view(master_dataframe: pd.DataFrame) -> None:
    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Fully Updated Master Sheet</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_columns = [column_name for column_name in MASTER_VIEW_DEFAULT_COLUMNS if column_name in master_dataframe.columns]
    display_dataframe = master_dataframe[display_columns].copy()

    numeric_columns = [
        column_name
        for column_name in [
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

    st.dataframe(
        display_dataframe,
        use_container_width=True,
        hide_index=True,
        height=FINAL_TABLE_HEIGHT,
    )
