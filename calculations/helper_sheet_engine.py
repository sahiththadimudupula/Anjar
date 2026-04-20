from __future__ import annotations

import pandas as pd

from config.workbook_config import HELPER_SHEET_MAPPING


def get_helper_sheet_configs(business_name: str) -> list[dict[str, str]]:
    return HELPER_SHEET_MAPPING.get(business_name, [])


def get_helper_dataframes_for_business(
    business_name: str,
    helper_dataframes: dict[str, pd.DataFrame],
) -> list[tuple[dict[str, str], pd.DataFrame]]:
    helper_views: list[tuple[dict[str, str], pd.DataFrame]] = []

    for helper_config in get_helper_sheet_configs(business_name):
        helper_sheet_name = helper_config["sheet_name"]
        if helper_sheet_name in helper_dataframes:
            helper_views.append((helper_config, helper_dataframes[helper_sheet_name]))

    return helper_views


def apply_helper_write_back(
    working_master_dataframe: pd.DataFrame,
    helper_dataframes: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    return working_master_dataframe, helper_dataframes
