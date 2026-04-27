# Anjar Manpower Engine

Streamlit planning engine for chairman-demo-ready manpower planning.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Workbook flow

- Original source workbook: `input/Anjar_manning.xlsx`
- Live editable workbook: `working/Anjar_manning_live.xlsx`
- Freeze writes current edits to the live workbook and creates an archive copy in `output/`
- Reset reloads the live workbook from the original input workbook
