from __future__ import annotations

import streamlit as st

from config.constants import APP_SUBTITLE, APP_TITLE


def render_page_header() -> None:
    st.markdown(
        f"""
        <div class="engine-shell">
            <div class="engine-title">{APP_TITLE}</div>
            <div class="engine-subtitle">{APP_SUBTITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_cards(metric_cards: list[dict[str, str]]) -> None:
    columns = st.columns(len(metric_cards))
    for column, card in zip(columns, metric_cards):
        with column:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-card-label">{card['label']}</div>
                    <div class="summary-card-value">{card['value']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
