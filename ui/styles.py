from __future__ import annotations

import streamlit as st

from config.ui_config import (
    BACKGROUND,
    BORDER_COLOR,
    LIGHT_BLUE,
    NAVY_TEXT,
    PANEL_SHADOW,
    PRIMARY_BLUE,
    RADIUS_LARGE,
    RADIUS_MEDIUM,
    SECONDARY_BLUE,
    SLATE_TEXT,
    WHITE,
)


def apply_global_styles() -> None:
    st.markdown(
        f"""
        <style>
            #MainMenu {{visibility: hidden;}}
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            [data-testid="stToolbar"] {{display: none;}}
            [data-testid="stDecoration"] {{display: none;}}
            .stApp {{
                background: {BACKGROUND};
            }}
            .block-container {{
                padding-top: 0.6rem;
                padding-bottom: 1.5rem;
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }}
            .engine-shell {{
                background: transparent;
                border: none;
                border-radius: 0;
                padding: 0.15rem 0 0.35rem 0;
                box-shadow: none;
                margin-bottom: 0.55rem;
            }}
            .engine-title {{
                font-size: 2.1rem;
                font-weight: 800;
                color: {PRIMARY_BLUE};
                margin-bottom: 0.15rem;
                letter-spacing: -0.02em;
            }}
            .engine-subtitle {{ display: none; }}
            .summary-card {{
                background: linear-gradient(180deg, #ffffff 0%, #f3f8ff 100%);
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                padding: 1rem 1.05rem;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 0.8rem;
            }}
            .summary-card-label {{
                font-size: 0.82rem;
                color: {SLATE_TEXT};
                font-weight: 700;
                margin-bottom: 0.32rem;
            }}
            .summary-card-value {{
                font-size: 1.55rem;
                color: {NAVY_TEXT};
                font-weight: 800;
                line-height: 1.1;
            }}
            .section-panel {{
                background: {WHITE};
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_LARGE};
                padding: 0.65rem 0.95rem 0.85rem 0.95rem;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 1rem;
            }}
            .section-strip {{
                background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_BLUE} 100%);
                color: {WHITE};
                padding: 0.82rem 1rem;
                border-radius: {RADIUS_MEDIUM};
                font-size: 1rem;
                font-weight: 750;
                margin-bottom: 0.75rem;
            }}
            .summary-banner {{
                background: {LIGHT_BLUE};
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                padding: 0.75rem 0.95rem;
                margin-bottom: 0.8rem;
            }}
            .summary-banner-text {{
                color: {NAVY_TEXT};
                font-weight: 700;
                font-size: 0.78rem;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.65rem;
                background: transparent;
                padding: 0.15rem 0 0.6rem 0;
            }}
            .stTabs [data-baseweb="tab"] {{
                height: 3rem;
                border-radius: 999px;
                background: {WHITE};
                border: 1px solid {BORDER_COLOR};
                color: {NAVY_TEXT};
                font-weight: 700;
                padding: 0 1.15rem;
            }}
            .stTabs [aria-selected="true"] {{
                background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_BLUE} 100%);
                color: {WHITE} !important;
                border: 1px solid {PRIMARY_BLUE};
            }}
            .stButton > button {{
                border-radius: 999px;
                height: 2.8rem;
                border: 1px solid {PRIMARY_BLUE};
                font-weight: 700;
                box-shadow: none;
            }}
            .stButton > button[kind="secondary"] {{
                background: #ffffff;
                color: #0f172a;
            }}
            .stButton > button[kind="primary"] {{
                background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_BLUE} 100%);
                color: #ffffff;
            }}
            .freeze-button button {{
                background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_BLUE} 100%);
                color: {WHITE};
            }}
            .secondary-button button {{
                background: {WHITE};
                color: {NAVY_TEXT};
            }}
            .stExpander {{
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                background: {WHITE};
            }}
            .stExpander summary {{
                color: {NAVY_TEXT};
                font-weight: 700;
                background: {LIGHT_BLUE};
                border-radius: {RADIUS_MEDIUM};
            }}
            .filter-shell {{
                background: {WHITE};
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_LARGE};
                padding: 0.9rem 1rem 0.3rem 1rem;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 1rem;
            }}
            div[data-testid="stDataEditor"] {{
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                overflow: hidden;
                background: #ffffff !important;
            }}
            div[data-testid="stDataEditor"] * {{
                color: #111111 !important;
            }}
            div[data-testid="stDataEditor"] input,
            div[data-testid="stDataEditor"] textarea,
            div[data-testid="stDataEditor"] [role="gridcell"],
            div[data-testid="stDataEditor"] [role="columnheader"],
            div[data-testid="stDataEditor"] section,
            div[data-testid="stDataEditor"] canvas {{
                background: #ffffff !important;
                color: #111111 !important;
            }}
            .html-table-shell {{
                background: #ffffff;
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                overflow: hidden;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 0.85rem;
            }}
            .html-table-caption {{
                background: #eff6ff;
                color: #0f172a;
                font-weight: 700;
                padding: 0.7rem 0.95rem;
                border-bottom: 1px solid {BORDER_COLOR};
            }}
            .html-table-scroll {{
                overflow: auto;
                background: #ffffff;
            }}
            table.executive-table {{
                width: max-content;
                border-collapse: collapse;
                background: #ffffff;
                color: #111111;
                font-size: 0.78rem;
            }}
            table.executive-table thead th {{
                position: sticky;
                top: 0;
                z-index: 1;
                background: #eff6ff;
                color: #0f172a;
                text-align: left;
                padding: 0.45rem 0.5rem;
                border-bottom: 1px solid {BORDER_COLOR};
                font-weight: 700;
                white-space: nowrap;
                max-width: 210px;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            table.executive-table tbody td {{
                background: #ffffff;
                color: #111111;
                padding: 0.38rem 0.5rem;
                border-bottom: 1px solid #e5edf8;
                white-space: nowrap;
                max-width: 210px;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            table.executive-table tbody tr.total-row td {{
                background: #f8fbff;
                font-weight: 800;
                color: #0f172a;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
