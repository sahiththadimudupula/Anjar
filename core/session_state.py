from __future__ import annotations

import streamlit as st

from config.constants import PENDING_STATUS


def initialize_session_state(
    master_dataframe,
    helper_dataframes,
    input_workbook_path: str,
    working_workbook_path: str,
) -> None:
    if "working_master_dataframe" not in st.session_state:
        st.session_state.working_master_dataframe = master_dataframe.copy()

    if "original_master_dataframe" not in st.session_state:
        st.session_state.original_master_dataframe = master_dataframe.copy()

    if "helper_dataframes" not in st.session_state:
        st.session_state.helper_dataframes = helper_dataframes

    if "freeze_status" not in st.session_state:
        st.session_state.freeze_status = PENDING_STATUS

    if "last_freeze_timestamp" not in st.session_state:
        st.session_state.last_freeze_timestamp = None

    if "input_workbook_path" not in st.session_state:
        st.session_state.input_workbook_path = input_workbook_path

    if "working_workbook_path" not in st.session_state:
        st.session_state.working_workbook_path = working_workbook_path


def refresh_session_state(master_dataframe, helper_dataframes) -> None:
    st.session_state.working_master_dataframe = master_dataframe.copy()
    st.session_state.original_master_dataframe = master_dataframe.copy()
    st.session_state.helper_dataframes = helper_dataframes


def clear_ui_state() -> None:
    keys_to_delete = [
        key
        for key in list(st.session_state.keys())
        if key.endswith("_editor")
        or key.endswith("_section_filter")
        or key.endswith("_designation_filter")
        or key.endswith("_machine_search")
        or key.endswith("_remarks_search")
        or key.endswith("_reset_filters")
        or key.endswith("_reset_button")
    ]
    for key in keys_to_delete:
        del st.session_state[key]
