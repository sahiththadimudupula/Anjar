from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st


TABLE_CSS = """
<style>
    body {
        margin: 0;
        padding: 0;
        background: #ffffff;
        font-family: Inter, Segoe UI, Arial, sans-serif;
    }
    .html-table-shell {
        background: #ffffff;
        border: 1px solid #d8e4f3;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }
    .html-table-shell.compact-table-shell {
        width: fit-content;
        max-width: 100%;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .html-table-shell.full-table-shell {
        width: 100%;
        max-width: 100%;
        display: block;
    }
    .html-table-caption {
        background: #eef4ff;
        color: #0f172a;
        font-weight: 700;
        padding: 8px 10px;
        border-bottom: 1px solid #d8e4f3;
        font-size: 12.5px;
    }
    .html-table-scroll {
        overflow: auto;
        background: #ffffff;
    }
    .compact-table-shell .html-table-scroll {
        width: auto;
        max-width: 100%;
    }
    .full-table-shell .html-table-scroll {
        width: 100%;
    }
    .executive-table {
        width: max-content;
        border-collapse: collapse;
        background: #ffffff;
        color: #111111;
        font-size: 12.5px;
        line-height: 1.2;
    }
    .executive-table thead th {
        position: sticky;
        top: 0;
        z-index: 1;
        background: #eef4ff;
        color: #111111;
        text-align: left;
        padding: 7px 8px;
        border-bottom: 1px solid #d8e4f3;
        border-right: 1px solid #e3edf8;
        font-weight: 700;
        white-space: nowrap;
        max-width: 210px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .executive-table tbody td {
        background: #ffffff;
        color: #111111;
        padding: 6px 8px;
        border-bottom: 1px solid #edf2f8;
        border-right: 1px solid #f0f4fa;
        white-space: nowrap;
        max-width: 210px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .executive-table tbody tr.total-row td {
        background: #f7fbff;
        color: #0f172a;
        font-weight: 800;
    }
</style>
"""


def _format_cell_value(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return escape(str(value))


def _build_table_html(
    dataframe: pd.DataFrame,
    *,
    height: int | None = None,
    caption: str | None = None,
    compact: bool = True,
) -> str:
    caption_html = ""
    if caption:
        caption_html = f'<div class="html-table-caption">{escape(caption)}</div>'

    header_html = "".join(
        f'<th title="{escape(str(column_name))}">{escape(str(column_name))}</th>'
        for column_name in dataframe.columns
    )
    body_rows: list[str] = []

    for _, row in dataframe.iterrows():
        is_total_row = any(str(cell_value).strip() == "Total" for cell_value in row.tolist())
        row_class = "total-row" if is_total_row else ""
        cell_html = "".join(
            f'<td class="{row_class}" title="{_format_cell_value(cell_value)}">{_format_cell_value(cell_value)}</td>'
            for cell_value in row.tolist()
        )
        body_rows.append(f'<tr class="{row_class}">{cell_html}</tr>')

    body_html = "".join(body_rows)
    height_style = f"max-height:{height}px;" if height else ""
    shell_class = "compact-table-shell" if compact else "full-table-shell"
    wrapper_start = '<div style="width:100%; text-align:center;">' if compact else ""
    wrapper_end = "</div>" if compact else ""

    return f"""
    {TABLE_CSS}
    {wrapper_start}
    <div class="html-table-shell {shell_class}">
        {caption_html}
        <div class="html-table-scroll" style="{height_style}">
            <table class="executive-table">
                <thead>
                    <tr>{header_html}</tr>
                </thead>
                <tbody>
                    {body_html}
                </tbody>
            </table>
        </div>
    </div>
    {wrapper_end}
    """


def _calculate_render_height(dataframe: pd.DataFrame, max_height: int | None, caption: str | None) -> int:
    header_height = 48
    row_height = 48
    shell_padding = 22
    caption_height = 54 if caption else 0
    content_height = header_height + (len(dataframe) * row_height) + shell_padding

    if max_height is not None:
        content_height = min(content_height, max_height)

    minimum_height = 120 + caption_height
    return max(content_height + caption_height + 8, minimum_height)



def render_html_table(
    dataframe: pd.DataFrame,
    *,
    height: int | None = None,
    caption: str | None = None,
    compact: bool = True,
) -> None:
    if dataframe.empty:
        st.info("No rows found for the selected filters.")
        return

    table_html = _build_table_html(dataframe, height=height, caption=caption, compact=compact)
    st.html(table_html, width="stretch")
