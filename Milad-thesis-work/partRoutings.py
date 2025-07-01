import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max
from ProcessingTask import PartRoutingsWithFullData, buildProcessingTasksDF  

def extract_part_routings(processing_tasks_df):
    """
    Generates Part Routings dataframe from Processing Tasks.
    Returns PartType, PartDestinationID, Machine (with 'Input@'), and Process columns.
    """
    if 'Process' not in processing_tasks_df.columns or 'TaskName' not in processing_tasks_df.columns:
        raise ValueError("Missing required columns in processing_tasks_df")

    # Extract PartType from TaskName (e.g., ANC101_1_SLOT_5 → ANC101)
    processing_tasks_df['PartType'] = processing_tasks_df['TaskName'].str.extract(r'(^[^_]+)')

    # Remove duplicates: one row per PartType + Process
    routing_df = processing_tasks_df[['PartType', 'Process']].drop_duplicates()

    # Extract machine name from Process and add "Input@" prefix
    routing_df['Machine'] = routing_df['Process'].apply(lambda p: f"Input@{p.split('_', maxsplit=2)[-1]}")

    # Assign sequential PartDestinationID per PartType
    routing_df['PartDestinationID'] = routing_df.groupby('PartType').cumcount() + 1

    # Reorder columns
    routing_df = routing_df[['PartType', 'PartDestinationID', 'Machine', 'Process']]

    return routing_df.reset_index(drop=True)

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

        # Extract PartRoutings from ProcessingTasks
        final_part_routing_df = extract_part_routings(processing_tasks_df)

        # Print result
        print(final_part_routing_df)
