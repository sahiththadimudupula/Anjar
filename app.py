from __future__ import annotations

import streamlit as st

from calculations.helper_sheet_engine import get_helper_dataframes_for_business
from calculations.summary_calculations import build_business_summary, build_executive_metrics
from config.constants import APP_TITLE, BUSINESS_TABS, MASTER_SHEET_NAME, SUCCESS_STATUS
from config.workbook_config import HELPER_SHEET_MAPPING
from core.excel_io import (
    load_helper_dataframes,
    load_master_dataframe,
    resolve_workbook_path,
    workbook_exists,
)
from core.filters import apply_business_filters
from core.session_state import initialize_session_state
from core.write_back import write_dataframe_back_to_excel
from ui.filter_bar import render_filter_bar
from ui.header import render_page_header, render_summary_cards
from ui.helper_tables import render_helper_sheet
from ui.master_sheet_view import render_master_sheet_view
from ui.section_tables import render_section_tables
from ui.styles import apply_global_styles
from ui.summary_table import render_business_summary_table


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def load_engine_data(workbook_path: str):
    master_dataframe = load_master_dataframe(workbook_path, MASTER_SHEET_NAME)
    helper_sheet_names = sorted(
        {
            helper_sheet_config["sheet_name"]
            for helper_sheet_configs in HELPER_SHEET_MAPPING.values()
            for helper_sheet_config in helper_sheet_configs
        }
    )
    helper_dataframes = load_helper_dataframes(workbook_path, helper_sheet_names)
    return master_dataframe, helper_dataframes


def render_freeze_controls() -> None:
    action_columns = st.columns([0.74, 0.12, 0.14])

    with action_columns[1]:
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button("Reset Draft", use_container_width=True):
            st.session_state.working_master_dataframe = st.session_state.original_master_dataframe.copy()
            st.session_state.freeze_status = "Draft"
            st.session_state.last_freeze_timestamp = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with action_columns[2]:
        st.markdown('<div class="freeze-button">', unsafe_allow_html=True)
        if st.button("Freeze Plan", use_container_width=True):
            _, frozen_copy_path = write_dataframe_back_to_excel(
                st.session_state.working_master_dataframe,
                st.session_state.workbook_path,
            )
            load_engine_data.clear()
            st.session_state.freeze_status = SUCCESS_STATUS
            st.session_state.last_freeze_timestamp = frozen_copy_path.name
            st.success(
                f"Plan frozen successfully. Updated workbook saved in input and archived as {frozen_copy_path.name}."
            )
        st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    apply_global_styles()

    workbook_path = resolve_workbook_path()
    if not workbook_exists(str(workbook_path)):
        st.error(f"Workbook not found at: {workbook_path}")
        st.stop()

    master_dataframe, helper_dataframes = load_engine_data(str(workbook_path))
    initialize_session_state(master_dataframe, helper_dataframes, str(workbook_path))

    render_page_header()
    metric_cards = build_executive_metrics(
        st.session_state.working_master_dataframe,
        st.session_state.freeze_status,
    )
    render_summary_cards(metric_cards)
    render_freeze_controls()

    all_tabs = st.tabs(BUSINESS_TABS + ["Final Master Sheet"])

    for tab_index, business_name in enumerate(BUSINESS_TABS):
        with all_tabs[tab_index]:
            business_dataframe = st.session_state.working_master_dataframe[
                st.session_state.working_master_dataframe["Business"].astype(str) == business_name
            ].copy()

            selected_sections, selected_designations, machine_search_text, remarks_search_text = render_filter_bar(
                business_name,
                business_dataframe,
            )

            filtered_business_dataframe = apply_business_filters(
                business_dataframe,
                selected_sections,
                selected_designations,
                machine_search_text,
                remarks_search_text,
            )

            summary_dataframe = build_business_summary(filtered_business_dataframe)
            render_business_summary_table(summary_dataframe)
            render_section_tables(business_name, filtered_business_dataframe)

            helper_views = get_helper_dataframes_for_business(
                business_name,
                st.session_state.helper_dataframes,
            )
            for helper_config, helper_dataframe in helper_views:
                render_helper_sheet(helper_config["display_name"], helper_dataframe)

    with all_tabs[-1]:
        render_master_sheet_view(st.session_state.working_master_dataframe)

        if st.session_state.last_freeze_timestamp:
            st.info(f"Last frozen file: {st.session_state.last_freeze_timestamp}")


if __name__ == "__main__":
    main()
