from __future__ import annotations

import streamlit as st

from config.constants import PENDING_STATUS


def initialize_session_state(
    master_dataframe,
    helper_dataframes,
    workbook_path: str,
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

    if "workbook_path" not in st.session_state:
        st.session_state.workbook_path = workbook_path
