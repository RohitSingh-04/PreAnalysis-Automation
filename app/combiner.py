import pandas as pd

def combined_files(detect_files):
    if len(detect_files):
        frames = []

        for file in detect_files:
            df = pd.read_excel(file, skiprows=1)
            df = df.drop(df.columns[0], axis=1)
            frames.append(df)

        combined = pd.concat(frames, ignore_index=True, sort=False)
        combined.to_excel("combined.xlsx", index=False)

        print(f"Combined {len(detect_files)} files into combined.xlsx ({len(combined)} rows).")
        return "combined.xlsx"

    else:
        print("no files found")
