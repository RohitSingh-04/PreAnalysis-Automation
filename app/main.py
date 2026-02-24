from app import combiner, deduper, cntr, cst_osdd, settings, excel_writer
import pandas as pd
from pathlib import Path

def start_app(filenames:list, input_dir:str):

    input_dir = Path(input_dir)

    # i tried this but i think this will be not optimal as the loop is again running in the function specified
    # combined_data = combiner.combined_files(list(map(lambda x: input_dir/x, filenames)))

    # so adding the logic there instead of using map
    combined_data = combiner.combined_files(filenames, input_dir)

    output_path = input_dir / settings.OUTPUT_DIR

    output_path.mkdir(parents=True, exist_ok=True)

    if combined_data is not None and not combined_data.empty:
        counterparty_informations = deduper.deduper(combined_data, mode=settings.COUNTERPARTY)

        uniques = deduper.deduper(combined_data, mode=settings.DUPER)

        cntr.detect_counterparty(counterparty_informations, output_path / 'counterparty_OSDD.html')
        cst_osdd.detect_customer(uniques, output_path / 'customer_OSDD.html')

        datas = (combined_data, counterparty_informations, uniques)
        sheetnames = ("Raw", "Counterparty Informations", "De Dupe")

        #write into one workbook now
        excel_writer.write_excel(output_path / 'Combined Alerted Transasctions.xlsx', datas, sheetnames)

    else:
        print("not valid")