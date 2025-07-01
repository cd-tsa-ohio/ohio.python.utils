import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max
from ProcessingTask import PartRoutingsWithFullData, buildProcessingTasksDF  

def extract_unique_processes(processing_tasks_df):
    """
    Returns a DataFrame with only the unique 'Process' names as a single column.
    """
    if 'Process' not in processing_tasks_df.columns:
        raise ValueError("Input DataFrame must contain a 'Process' column.")

    # Extract unique process names only
    unique_processes = processing_tasks_df[['Process']].drop_duplicates().reset_index(drop=True)
    return unique_processes

# === Example usage if running directly ===
if __name__ == "__main__":
    # Get file names from ou.getFiles()
    file_names = ou.getFiles()

    # Build PartRoutings DataFrame
    part_routings_df = PartRoutingsWithFullData(file_names)

    # If no valid data, notify user
    if part_routings_df.empty:
        print("No valid part routings found. Please check your CSV files.")
    else:
        # Build ProcessingTasks DataFrame
        processing_tasks_df = buildProcessingTasksDF(part_routings_df)

        # Extract unique Processes
        processes_df = extract_unique_processes(processing_tasks_df)

        # Print result
        print(processes_df)
