import pandas as pd
from app.settings import TRANSACTION_AMOUNT, CURRENCY_FORMAT
def validate_input_data_file(sheet_names: tuple, datas: tuple):
    return len(sheet_names) == len(datas)

def write_excel(output_dir: str, datas: tuple[pd.DataFrame], sheet_names: tuple[str]):
    if validate_input_data_file(sheet_names, datas):
        with pd.ExcelWriter(output_dir, engine="openpyxl") as excelwriter:
            for i in range(len(datas)):
                df = datas[i].copy()
                
                text_cols = [c for c in df.columns if c != TRANSACTION_AMOUNT]
                df[text_cols] = df[text_cols].astype(str)
                
                df.to_excel(excelwriter, index=False, sheet_name=sheet_names[i])
                current_sheet = excelwriter.sheets[sheet_names[i]]

                for col in current_sheet.columns:
                    max_length = 0
                    column_letter = col[0].column_letter
                    header_value = col[0].value

                    for cell in col:
                        if header_value == TRANSACTION_AMOUNT and cell.row > 1:
                            cell.number_format = CURRENCY_FORMAT
                        elif cell.row > 1:
                            cell.number_format = '@'

                        try:
                            if cell.value:
                                max_length = max(max_length, len(str(cell.value)))
                        except:
                            pass
                    
                    adjusted_width = (max_length + 2) #padding 2 for the column
                    
                    current_sheet.column_dimensions[column_letter].width = adjusted_width