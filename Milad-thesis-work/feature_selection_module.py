import pandas as pd

def feature_selection_max(df):
    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and select the row with maximum 'Processing Time' for each group
        max_processing_time_df = df.loc[df.groupby('Feature Name')['Processing Time'].idxmax()]

        # Reset index for a clean output DataFrame
        max_processing_time_df = max_processing_time_df.reset_index(drop=True)
        
        return max_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def feature_selection_min(df):
   
    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and select the row with minimum 'Processing Time' for each group
        min_processing_time_df = df.loc[df.groupby('Feature Name')['Processing Time'].idxmin()]

        # Reset index for a clean output DataFrame
        min_processing_time_df = min_processing_time_df.reset_index(drop=True)
        
        return min_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
def feature_selection_median(df):

    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and calculate the median processing time
        median_processing_time_df = df.groupby('Feature Name', as_index=False)['Processing Time'].median()

        # Rename the column for clarity
        median_processing_time_df.rename(columns={'Processing Time': 'Median Processing Time'}, inplace=True)
        
        return median_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error