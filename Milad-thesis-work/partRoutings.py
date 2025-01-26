import pandas as pd
import ou_file_utils as ou
from parttable import partTable
from feature_selection_module import feature_selection_max

def PartRoutings(partName,input_df):
    output_df = 
    try:
        
        # Create PartDestinationID based on the number of rows in the input dataframe
        input_df['PartDestinationID'] = range(1, len(input_df) + 1)

        # Create Machine column with "Input@" prefix
        input_df['Machine'] = "Input@" + input_df['Machine']

        # Create Process column by combining parttype, PartDestinationID, and Machine
        input_df['Process'] = partName + "_" + input_df['PartDestinationID'].astype(str) + "_" + input_df['Machine']

        # Create Process column by combining parttype, PartDestinationID, and Machine
        input_df['Process'] = input_df.apply(
            lambda row: f"{partName}_{row['PartDestinationID']}_{row['Machine']}", axis=1
        )

        # Return the resulting dataframe with the required columns
        return input_df[[ 'PartDestinationID', 'Machine', 'Process']].assign(partType=partName)

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

if __name__ == "__main__":
    # Load the input DataFrame (replace with your actual loading logic)
    input_data = ou.getDataFrame()

    # Apply feature_selection_max to prepare the input for PartRoutings
    max_processing_time_df = feature_selection_max(input_data)

    # Generate the PartRoutings output
    part_routings_df = PartRoutings("xxx",max_processing_time_df)
 
    # Print the resulting DataFrame
    print(part_routings_df)