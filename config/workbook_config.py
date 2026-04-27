from config.constants import BUSINESS_TABS, MASTER_SHEET_NAME

WORKBOOK_LAYOUT = {
    "master_sheet_name": MASTER_SHEET_NAME,
    "business_tabs": BUSINESS_TABS,
}

TAB_BUSINESS_MAPPING = {
    "Spinning": ["Spinning", "Open End"],
    "Terry Towel": ["Terry Towel"],
    "Bedsheet": ["Bedsheet"],
    "WHSL Plant": ["WHSL Plant"],
    "Other Sections": ["Plant Support", "Central Admin", "Trainees"],
}

BUSINESS_VALUE_NORMALIZATION = {
    "Sheeting": "Bedsheet",
}

HELPER_SHEET_MAPPING = {
    "Spinning": [
        {
            "sheet_name": "Spinning",
            "display_name": "Spinning Helper Sheet",
            "mode": "display_only",
        }
    ],
    "Terry Towel": [],
    "Bedsheet": [],
    "WHSL Plant": [],
    "Other Sections": [],
}

SUMMARY_EDITABLE = False
SUMMARY_DRIVER_MAPPING = {}
WRITE_BACK_FUNCTION_MAPPING = {}
