# Anjar Manpower Engine

Chairman-demo-ready Streamlit planning engine for Welspun Anjar manpower planning.

## Features

- Premium blue/white executive UI
- Reads workbook directly from `input/Anjar_manning.xlsx`
- Tabs for:
  - Spinning
  - Terry Towel
  - Sheeting
- Section-wise summary at top of each business tab
- Separate section panels with compact and expanded views
- Editable fields:
  - `BE_Final_Manpower`
  - `General_Shift`
  - `Shift_A`
  - `Shift_B`
  - `Shift_C`
  - `Reliever`
  - `Remarks`
- Freeze button writes edits back to Excel
- Final Master Sheet tab shows the updated master sheet
- Helper sheet architecture included
- Business logic separated from UI

## Project Structure

```text
anjar_manpower_engine/
├── app.py
├── config/
├── core/
├── calculations/
├── ui/
├── input/
│   └── Anjar_manning.xlsx
├── output/
├── requirements.txt
└── README.md
```

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Source of truth is the `Anjar` sheet.
- Current helper mapping includes the `Spinning` sheet as a display-only helper inside the Spinning tab.
- Freeze updates the workbook in `input/Anjar_manning.xlsx` and also writes a timestamped copy to `output/`.
- The architecture is ready for future formula engines and sheet mappings without changing the UI.
