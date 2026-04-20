from config.constants import MASTER_SHEET_NAME

WORKBOOK_LAYOUT = {
    "master_sheet_name": MASTER_SHEET_NAME,
    "business_tabs": ["Spinning", "Terry Towel", "Sheeting"],
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
    "Sheeting": [],
}

SUMMARY_EDITABLE = False

SUMMARY_DRIVER_MAPPING = {}

WRITE_BACK_FUNCTION_MAPPING = {}
