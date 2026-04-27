from __future__ import annotations

import pandas as pd

from core.dataframe_utils import parse_machine_count
from core.totals import append_total_row


def build_business_summary(business_dataframe: pd.DataFrame) -> pd.DataFrame:
    summary_rows: list[dict[str, object]] = []

    for section_name, section_dataframe in business_dataframe.groupby("Section", sort=False):
        parsed_machine_count_series = section_dataframe["Machine_Count"].apply(parse_machine_count)
        parsed_machine_count_total = parsed_machine_count_series.dropna().sum()

        summary_rows.append(
            {
                "Section": section_name,
                "Machine_Count": float(parsed_machine_count_total) if not pd.isna(parsed_machine_count_total) else None,
                "BE_Final_Manpower": pd.to_numeric(section_dataframe["BE_Final_Manpower"], errors="coerce").sum(),
            }
        )

    summary_dataframe = pd.DataFrame(summary_rows)
    if summary_dataframe.empty:
        return summary_dataframe

    return append_total_row(summary_dataframe, label_column="Section")
