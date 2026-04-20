from __future__ import annotations

import pandas as pd

from core.dataframe_utils import parse_machine_count


def build_business_summary(business_dataframe: pd.DataFrame) -> pd.DataFrame:
    summary_rows: list[dict[str, object]] = []

    for section_name, section_dataframe in business_dataframe.groupby("Section", sort=False):
        parsed_machine_count_series = section_dataframe["Machine_Count"].apply(parse_machine_count)
        parsed_machine_count_total = parsed_machine_count_series.dropna().sum()

        summary_rows.append(
            {
                "Section": section_name,
                "Machine_Count": parsed_machine_count_total if not pd.isna(parsed_machine_count_total) else None,
                "BE_Final_Manpower": pd.to_numeric(
                    section_dataframe["BE_Final_Manpower"],
                    errors="coerce",
                ).sum(),
            }
        )

    return pd.DataFrame(summary_rows)


def build_executive_metrics(master_dataframe: pd.DataFrame, freeze_status: str) -> list[dict[str, str]]:
    parsed_machine_count_total = master_dataframe["Machine_Count"].apply(parse_machine_count).dropna().sum()
    total_final_manpower = pd.to_numeric(master_dataframe["BE_Final_Manpower"], errors="coerce").sum()

    return [
        {"label": "Total Sections", "value": f"{master_dataframe['Section'].nunique():,.0f}"},
        {"label": "Parsed Machine Count", "value": f"{parsed_machine_count_total:,.2f}"},
        {"label": "Total Final Manpower", "value": f"{total_final_manpower:,.2f}"},
        {"label": "Freeze Status", "value": freeze_status},
    ]
