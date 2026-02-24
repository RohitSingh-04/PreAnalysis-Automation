import pandas as pd
from pathlib import Path

def combined_files(detect_files: list, input_dir: Path) -> pd.DataFrame:
    if len(detect_files):
        frames = []

        for file in detect_files:
            #changed this to search on the dir user inputed
            
            df = pd.read_excel(input_dir/file, skiprows=1)
            df = df.drop(df.columns[0], axis=1)
            frames.append(df)

        combined = pd.concat(frames, ignore_index=True, sort=False)
        #i added this to convert the text dollar values to numeric values
        combined["Transaction Amount"] = combined["Transaction Amount"].str.replace("$", '', regex=False).str.replace(',', '', regex=False).astype(float)
        
        return combined

    else:
        raise ValueError
