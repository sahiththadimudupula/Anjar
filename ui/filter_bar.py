from __future__ import annotations

import streamlit as st

from core.dataframe_utils import ordered_unique


def render_filter_bar(business_name: str, business_dataframe):
    section_options = ordered_unique(business_dataframe["Section"])
    designation_options = ordered_unique(business_dataframe["Designation"])

    state_prefix = business_name.lower().replace(" ", "_")

    if st.session_state.get(f"{state_prefix}_reset_filters", False):
        st.session_state[f"{state_prefix}_section_filter"] = []
        st.session_state[f"{state_prefix}_designation_filter"] = []
        st.session_state[f"{state_prefix}_machine_search"] = ""
        st.session_state[f"{state_prefix}_remarks_search"] = ""
        st.session_state[f"{state_prefix}_reset_filters"] = False

    st.markdown('<div class="filter-shell">', unsafe_allow_html=True)
    filter_columns = st.columns([1.3, 1.3, 1.2, 1.2, 0.7])

    with filter_columns[0]:
        selected_sections = st.multiselect(
            "Section Filter",
            options=section_options,
            key=f"{state_prefix}_section_filter",
            placeholder="All sections",
        )

    with filter_columns[1]:
        selected_designations = st.multiselect(
            "Designation Filter",
            options=designation_options,
            key=f"{state_prefix}_designation_filter",
            placeholder="All designations",
        )

    with filter_columns[2]:
        machine_search_text = st.text_input(
            "Machine Search",
            key=f"{state_prefix}_machine_search",
            placeholder="Type machine name",
        )

    with filter_columns[3]:
        remarks_search_text = st.text_input(
            "Remarks Search",
            key=f"{state_prefix}_remarks_search",
            placeholder="Type remarks",
        )

    with filter_columns[4]:
        st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
        if st.button("Reset", key=f"{state_prefix}_reset_button", width="stretch"):
            st.session_state[f"{state_prefix}_reset_filters"] = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return selected_sections, selected_designations, machine_search_text, remarks_search_text
