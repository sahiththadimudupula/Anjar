from __future__ import annotations

import streamlit as st

from core.formatting import build_formatted_display_dataframe


def render_helper_sheet(helper_display_name: str, helper_dataframe) -> None:
    with st.expander(f"View {helper_display_name}", expanded=False):
        display_dataframe = build_formatted_display_dataframe(
            helper_dataframe,
            numeric_columns=[],
        )
        st.dataframe(
            display_dataframe,
            use_container_width=True,
            hide_index=True,
            height=320,
        )
