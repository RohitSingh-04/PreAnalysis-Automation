from app import combiner, deduper, cntr, cst_osdd
import pandas as pd

filename = combiner.combined_files()

COUNTERPARTY = 0
DUPER = 1

if filename:
    df = pd.read_excel(filename)
    counterparty_informations = deduper.deduper(df, mode=COUNTERPARTY)
    counterparty_informations.to_excel("counterparty.xlsx", index=False, sheet_name = "counterparty")
    cntr.detect_counterparty("counterparty.xlsx")
    uniques = deduper.deduper(df, mode=DUPER)
    uniques.to_excel("uniques.xlsx", index = False, sheet_name = "unique")
    cst_osdd.detect_customer("uniques.xlsx")

else:
    print("not valid")