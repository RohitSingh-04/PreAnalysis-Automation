import pandas as pd
from app.settings import TRANSACTION_AMOUNT, CURRENCY_FORMAT
def validate_input_data_file(sheet_names: tuple, datas: tuple):
    return len(sheet_names) == len(datas)

def write_excel(output_dir:str, datas: tuple[pd.DataFrame], sheet_names: tuple[str]):

    if validate_input_data_file(sheet_names, datas):

        with pd.ExcelWriter(output_dir, engine="openpyxl") as excelwriter:

            for i in range(len(datas)):

                datas[i].to_excel(excelwriter, index=False, sheet_name = sheet_names[i])
                
                current_sheet = excelwriter.sheets[sheet_names[i]]

                column = None

                for cell in current_sheet[1]:
                    if cell.value == TRANSACTION_AMOUNT:
                        column = cell.column_letter
                        break
                
                if column:
                    for cell in current_sheet[column]:
                        if cell.row>1:
                            cell.number_format=CURRENCY_FORMAT

