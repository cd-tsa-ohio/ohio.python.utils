import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from feature_selection_module import feature_selection_max

def getDataFramesWithNames():
    tk.Tk().withdraw()
    paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV Files", "*.csv")])
    return [(os.path.splitext(os.path.basename(p))[0], pd.read_csv(p)) for p in paths]

def PartRoutingsWithFilenames(named_dataframes):
    try:
        all_parts = []
        for name, df in named_dataframes:
            if 'Machine' not in df.columns:
                raise ValueError(f"Missing 'Machine' column in file: {name}")

            df = feature_selection_max(df).copy()
            df['PartType'] = name
            df['PartDestinationID'] = range(1, len(df) + 1)
            df['Machine'] = "Input@" + df['Machine'].astype(str)
            df['Process'] = df.apply(lambda r: f"{name}_{r['PartDestinationID']}_{r['Machine'].replace('Input@', '')}", axis=1)

            df = df[['PartType', 'PartDestinationID', 'Machine', 'Process']]
            df.loc[len(df)] = [name, len(df) + 1, 'Input@FinishedPart', f'{name}_Complete']
            all_parts.append(df)

        return pd.concat(all_parts, ignore_index=True)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    part_routings_df = PartRoutingsWithFilenames(getDataFramesWithNames())
    print(part_routings_df)



    