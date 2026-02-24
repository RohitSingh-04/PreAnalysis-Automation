from app import combiner, deduper, cntr, cst_osdd, settings
import pandas as pd


def start_app(filenames:list):

    filename = combiner.combined_files(filenames)

    if filename:
        df = pd.read_excel(filename)
        
        counterparty_informations = deduper.deduper(df, mode=settings.COUNTERPARTY)
        counterparty_informations.to_excel("counterparty.xlsx", index=False, sheet_name = "counterparty")

        cntr.detect_counterparty("counterparty.xlsx")

        uniques = deduper.deduper(df, mode=settings.DUPER)
        uniques.to_excel("uniques.xlsx", index = False, sheet_name = "unique")
        cst_osdd.detect_customer("uniques.xlsx")

    else:
        print("not valid")