from __future__ import annotations

import re

import pandas as pd

from config.workbook_config import BUSINESS_VALUE_NORMALIZATION


def normalize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    normalized_dataframe = dataframe.copy()
    normalized_dataframe.columns = [str(column_name).strip() for column_name in normalized_dataframe.columns]
    return normalized_dataframe


def normalize_business_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    normalized_dataframe = dataframe.copy()
    if "Business" not in normalized_dataframe.columns:
        return normalized_dataframe
    normalized_dataframe["Business"] = normalized_dataframe["Business"].replace(BUSINESS_VALUE_NORMALIZATION)
    return normalized_dataframe


def create_row_metadata(dataframe: pd.DataFrame, excel_row_start: int = 2) -> pd.DataFrame:
    metadata_dataframe = dataframe.copy().reset_index(drop=True)
    metadata_dataframe["__excel_row_number"] = metadata_dataframe.index + excel_row_start
    metadata_dataframe["__row_order"] = metadata_dataframe.index
    metadata_dataframe["__row_key"] = metadata_dataframe["__excel_row_number"].astype(str)
    return metadata_dataframe


def ordered_unique(values: pd.Series) -> list[str]:
    ordered_values: list[str] = []
    seen_values: set[str] = set()
    for value in values.dropna().tolist():
        text_value = str(value).strip()
        if text_value and text_value not in seen_values:
            seen_values.add(text_value)
            ordered_values.append(text_value)
    return ordered_values


def parse_machine_count(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None

    text_value = str(value).strip()
    if not text_value:
        return None

    allowed_prefix_characters = []
    for character in text_value:
        if character.isdigit() or character in {".", "&", "+", "-", " ", "/"}:
            allowed_prefix_characters.append(character)
            continue
        break

    prefix_text = "".join(allowed_prefix_characters).strip()
    if not prefix_text:
        return None

    numeric_matches = re.findall(r"\d+(?:\.\d+)?", prefix_text)
    if not numeric_matches:
        return None

    return float(sum(float(match) for match in numeric_matches))


def ensure_text_columns(dataframe: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    text_dataframe = dataframe.copy()
    for column_name in column_names:
        if column_name in text_dataframe.columns:
            text_dataframe[column_name] = text_dataframe[column_name].fillna("").astype(str)
    return text_dataframe
