from __future__ import annotations

import streamlit as st

from config.constants import HELPER_TABLE_HEIGHT
from core.formatting import build_formatted_display_dataframe
from ui.table_renderer import render_html_table


def render_helper_sheet(helper_display_name: str, helper_dataframe) -> None:
    with st.expander(f"View {helper_display_name}", expanded=False):
        display_dataframe = build_formatted_display_dataframe(helper_dataframe, numeric_columns=[])
        render_html_table(display_dataframe, height=HELPER_TABLE_HEIGHT)
