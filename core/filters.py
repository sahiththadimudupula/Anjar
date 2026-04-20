from __future__ import annotations

import pandas as pd


def apply_business_filters(
    business_dataframe: pd.DataFrame,
    selected_sections: list[str] | None,
    selected_designations: list[str] | None,
    machine_search_text: str,
    remarks_search_text: str,
) -> pd.DataFrame:
    filtered_dataframe = business_dataframe.copy()

    if selected_sections:
        filtered_dataframe = filtered_dataframe[filtered_dataframe["Section"].astype(str).isin(selected_sections)]

    if selected_designations:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Designation"].astype(str).isin(selected_designations)
        ]

    if machine_search_text:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Dept_Machine_Name"]
            .fillna("")
            .astype(str)
            .str.contains(machine_search_text, case=False, na=False)
        ]

    if remarks_search_text:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Remarks"]
            .fillna("")
            .astype(str)
            .str.contains(remarks_search_text, case=False, na=False)
        ]

    return filtered_dataframe.sort_values("__row_order").reset_index(drop=True)
