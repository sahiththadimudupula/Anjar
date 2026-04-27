from __future__ import annotations

import streamlit as st


def render_tab_cards(metric_cards: list[dict[str, str]]) -> None:
    columns = st.columns(len(metric_cards))
    for column, card in zip(columns, metric_cards):
        with column:
            st.markdown(
                f"""
                <div class="summary-card premium-kpi-card">
                    <div class="summary-card-label">{card['label']}</div>
                    <div class="summary-card-value">{card['value']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
