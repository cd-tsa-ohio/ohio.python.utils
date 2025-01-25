import pandas as pd
import ou_file_utils as ou
from parttable import partTable
from feature_selection_module import feature_selection_max

def PartRoutings(input_df):
    try:
        # Call partTable to get part type information
        part_table_df = partTable(input_df['Feature Name'].unique())  

        # Extract the part type from the ResourceName column in the partTable output
        parttype = part_table_df.loc[part_table_df['ResourceName'].notna(), 'ResourceName'].iloc[0]

        # Create PartDestinationID based on the number of rows in the input dataframe
        input_df['PartDestinationID'] = range(1, len(input_df) + 1)

        # Create Machine column with "Input@" prefix
        input_df['Machine'] = "Input@" + input_df['Machine']

        # Create Process column by combining parttype, PartDestinationID, and Machine
        input_df['Process'] = parttype + "_" + input_df['PartDestinationID'].astype(str) + "_" + input_df['Machine']

        # Create Process column by combining parttype, PartDestinationID, and Machine
        input_df['Process'] = input_df.apply(
            lambda row: f"{parttype}_{row['PartDestinationID']}_{row['Machine']}", axis=1
        )

        # Return the resulting dataframe with the required columns
        return input_df[[ 'PartDestinationID', 'Machine', 'Process']].assign(partType=parttype)

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

if __name__ == "__main__":
    # Load the input DataFrame (replace with your actual loading logic)
    input_data = ou.getDataFrame()

    # Apply feature_selection_max to prepare the input for PartRoutings
    max_processing_time_df = feature_selection_max(input_data)

    # Generate the PartRoutings output
    part_routings_df = PartRoutings(max_processing_time_df)

    # Print the resulting DataFrame
    print(part_routings_df)