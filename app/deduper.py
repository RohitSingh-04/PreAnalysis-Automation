import pandas as pd

modes = {0: ["Transaction ID", "Alert Information"], 1: ["Transaction ID"]}

def isValid(data: pd.DataFrame) -> bool:
    #we can implement checks here
    return True 

def deduper(data: pd.DataFrame, mode: int) -> pd.DataFrame:
    if isValid(data):
        unique = data.drop_duplicates(subset=modes[mode], keep="first")
        return unique
    else:
        raise ValueError