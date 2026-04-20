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
    SUCCESS_GREEN,
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
                padding-top: 1.3rem;
                padding-bottom: 2rem;
                max-width: 96rem;
            }}
            .engine-shell {{
                background: linear-gradient(180deg, rgba(255,255,255,0.72) 0%, rgba(234,244,255,0.60) 100%);
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_LARGE};
                padding: 1.1rem 1.25rem 0.95rem 1.25rem;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 1rem;
            }}
            .engine-title {{
                font-size: 2.1rem;
                font-weight: 800;
                color: {NAVY_TEXT};
                margin-bottom: 0.2rem;
                letter-spacing: -0.02em;
            }}
            .engine-subtitle {{
                font-size: 0.98rem;
                color: {SLATE_TEXT};
                margin-bottom: 0.15rem;
            }}
            .summary-card {{
                background: {WHITE};
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                padding: 1rem 1.05rem;
                box-shadow: {PANEL_SHADOW};
            }}
            .summary-card-label {{
                font-size: 0.82rem;
                color: {SLATE_TEXT};
                font-weight: 600;
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
                padding: 0.55rem 0.9rem 0.8rem 0.9rem;
                box-shadow: {PANEL_SHADOW};
                margin-bottom: 1rem;
            }}
            .section-strip {{
                background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_BLUE} 100%);
                color: {WHITE};
                padding: 0.80rem 1rem;
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
                font-size: 0.92rem;
            }}
            .status-good {{
                color: {SUCCESS_GREEN};
                font-weight: 700;
            }}
            div[data-testid="stDataFrame"] {{
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                overflow: hidden;
            }}
            div[data-testid="stDataEditor"] {{
                border: 1px solid {BORDER_COLOR};
                border-radius: {RADIUS_MEDIUM};
                overflow: hidden;
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
        </style>
        """,
        unsafe_allow_html=True,
    )
