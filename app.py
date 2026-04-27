from __future__ import annotations

import streamlit as st

from calculations.helper_sheet_engine import get_helper_dataframes_for_business
from calculations.summary_calculations import build_business_summary
from config.constants import APP_TITLE, BUSINESS_TABS, MASTER_SHEET_NAME, SUCCESS_STATUS
from config.workbook_config import HELPER_SHEET_MAPPING, TAB_BUSINESS_MAPPING
from core.excel_io import (
    ensure_working_workbook,
    load_helper_dataframes,
    load_master_dataframe,
    reset_working_workbook,
    resolve_input_workbook_path,
    workbook_exists,
)
from core.filters import apply_business_filters
from core.session_state import clear_ui_state, initialize_session_state, refresh_session_state
from core.totals import build_tab_kpis
from core.write_back import write_dataframe_back_to_excel
from ui.filter_bar import render_filter_bar
from ui.header import render_page_header
from ui.helper_tables import render_helper_sheet
from ui.master_sheet_view import render_master_sheet_view
from ui.section_tables import render_section_tables
from ui.styles import apply_global_styles
from ui.summary_table import render_business_summary_table
from ui.tab_cards import render_tab_cards

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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


def _reload_from_working_copy(working_workbook_path: str) -> None:
    master_dataframe, helper_dataframes = load_engine_data(working_workbook_path)
    refresh_session_state(master_dataframe, helper_dataframes)


def render_freeze_controls() -> None:
    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Plan Actions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, reset_col, freeze_col, _ = st.columns([3.2, 1.2, 1.4, 3.2])

    with reset_col:
        if st.button("Reset", key="bottom_reset_button", width="stretch"):
            working_workbook_path = reset_working_workbook(st.session_state.input_workbook_path)
            clear_ui_state()
            master_dataframe, helper_dataframes = load_engine_data(str(working_workbook_path))
            refresh_session_state(master_dataframe, helper_dataframes)
            st.session_state.working_workbook_path = str(working_workbook_path)
            st.session_state.freeze_status = "Draft"
            st.session_state.last_freeze_timestamp = None
            st.rerun()

    with freeze_col:
        if st.button("Freeze Plan", key="bottom_freeze_button", width="stretch"):
            _, frozen_copy_path = write_dataframe_back_to_excel(
                st.session_state.working_master_dataframe,
                st.session_state.working_workbook_path,
            )
            _reload_from_working_copy(st.session_state.working_workbook_path)
            st.session_state.freeze_status = SUCCESS_STATUS
            st.session_state.last_freeze_timestamp = frozen_copy_path.name if frozen_copy_path else None
            st.success("Plan frozen successfully.")


def _get_tab_dataframe(master_dataframe, business_name: str):
    business_values = TAB_BUSINESS_MAPPING.get(business_name, [business_name])
    return master_dataframe[master_dataframe["Business"].astype(str).isin(business_values)].copy()


def main() -> None:
    apply_global_styles()

    input_workbook_path = resolve_input_workbook_path()
    if not workbook_exists(input_workbook_path):
        st.error(f"Workbook not found at: {input_workbook_path}")
        st.stop()

    working_workbook_path = ensure_working_workbook(input_workbook_path)
    master_dataframe, helper_dataframes = load_engine_data(str(working_workbook_path))
    initialize_session_state(
        master_dataframe,
        helper_dataframes,
        str(input_workbook_path),
        str(working_workbook_path),
    )

    render_page_header()

    all_tabs = st.tabs(BUSINESS_TABS + ["Final Master Sheet"])

    for tab_index, business_name in enumerate(BUSINESS_TABS):
        with all_tabs[tab_index]:
            business_dataframe = _get_tab_dataframe(st.session_state.working_master_dataframe, business_name)

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

            render_tab_cards(build_tab_kpis(filtered_business_dataframe))
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
        render_master_sheet_view(
            st.session_state.working_master_dataframe,
            st.session_state.working_workbook_path,
        )
        if st.session_state.last_freeze_timestamp:
            st.info(f"Last frozen file: {st.session_state.last_freeze_timestamp}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    render_freeze_controls()


if __name__ == "__main__":
    main()
