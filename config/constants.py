APP_TITLE = "Anjar Manpower Engine"
APP_SUBTITLE = "Executive manpower planning"

INPUT_WORKBOOK_PATH = "input/Anjar_manning.xlsx"
MASTER_SHEET_NAME = "Anjar"
OUTPUT_DIRECTORY = "output"

BUSINESS_TABS = ["Spinning", "Terry Towel", "Sheeting"]

VISIBLE_COMPACT_COLUMNS = [
    "Section",
    "Dept_Machine_Name",
    "Designation",
    "BE_Final_Manpower",
]

EDITABLE_COLUMNS = [
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
    "Remarks",
]

SUMMARY_COLUMNS = [
    "Section",
    "Machine_Count",
    "BE_Final_Manpower",
]

PRIMARY_FILTER_COLUMNS = [
    "Section",
    "Designation",
    "Dept_Machine_Name",
    "Remarks",
]

EXECUTIVE_CARD_COLUMNS = [
    "Total Sections",
    "Parsed Machine Count",
    "Total Final Manpower",
    "Freeze Status",
]

MASTER_VIEW_DEFAULT_COLUMNS = [
    "Location",
    "Business",
    "Section",
    "Dept_Machine_Name",
    "Designation",
    "Machine_Count",
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
    "Remarks",
]

HIDDEN_SYSTEM_COLUMNS = [
    "__excel_row_number",
    "__row_order",
    "__row_key",
]

DEFAULT_DECIMAL_PLACES = 2
DATA_EDITOR_HEIGHT = 420
SUMMARY_TABLE_HEIGHT = 220
COMPACT_TABLE_HEIGHT = 220
FINAL_TABLE_HEIGHT = 640

SUCCESS_STATUS = "Frozen"
PENDING_STATUS = "Draft"
