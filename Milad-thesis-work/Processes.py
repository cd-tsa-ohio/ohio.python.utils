from partRoutings import getDataFramesWithNames, PartRoutingsWithFilenames
import pandas as pd

if __name__ == "__main__":
    named_dataframes = getDataFramesWithNames()
    part_routings_df = PartRoutingsWithFilenames(named_dataframes)

    # Extract only the 'Process' column as a DataFrame
    process_column_df = part_routings_df[['Process']]

    print(process_column_df)
    