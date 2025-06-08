import os
import pandas as pd
import random
import ou_file_utils as ou
from feature_selection_module import feature_selection_max

# === Helper function: extract part name from file path ===
def partName(file_path):
    return file_path[file_path.rfind('/') + 1 : file_path.rfind('.')]

# === Build Part Routings DataFrame with required columns ===
def PartRoutingsWithFullData(file_names):
    try:
        all_parts = []

        for file in file_names:
            # Get file path and part name
            file_path = file[0] if isinstance(file, tuple) else file
            name = partName(file_path)

            # Read CSV file
            df = pd.read_csv(file_path)

            # Check required columns
            required_columns = ['Feature Name', 'Machine', 'Tool', 'Processing Time']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"Skipping file {name}: missing columns {missing_columns}")
                continue  # Skip this file if columns are missing

            # Apply feature selection function
            df = feature_selection_max(df).copy()

            # Add PartType and PartDestinationID columns
            df['PartType'] = name
            df['PartDestinationID'] = range(1, len(df) + 1)

            # Prefix Machine with "Input@"
            df['Machine'] = "Input@" + df['Machine'].astype(str)

            # Build Process column: PartName_PartDestinationID_MachineName
            df['Process'] = df.apply(lambda r: f"{name}_{r['PartDestinationID']}_{r['Machine'].replace('Input@', '')}", axis=1)

            # Keep required columns — now including Feature Name
            df = df[['PartType', 'PartDestinationID', 'Feature Name', 'Machine', 'Process', 'Tool', 'Processing Time']]

            # Add a FinishedPart row for each part type
            df.loc[len(df)] = [name, len(df) + 1, 'FinishedPart', 'Input@FinishedPart', f'{name}_Complete', 'None', 0]

            # Append result to all_parts list
            all_parts.append(df)

        # Return combined dataframe
        return pd.concat(all_parts, ignore_index=True) if all_parts else pd.DataFrame()

    except Exception as e:
        print(f"Error in PartRoutingsWithFullData: {e}")
        return pd.DataFrame()

# === Build Processing Tasks DataFrame ===
def buildProcessingTasksDF(part_routings_df):
    result_rows = []

    # Group by PartType (one part type at a time)
    for part_type, group in part_routings_df.groupby('PartType'):
        prev_machine = None  # Track previous machine to manage TaskSeqNum
        task_seq_counter = 10
        machine_task_counter = {}  # Track number of tasks per machine

        # Iterate over rows for this part type
        for _, row in group.iterrows():
            machine = row['Machine']
            tool = row['Tool']
            proc_time = row['Processing Time']
            feature_name = row['Feature Name']

            # Increment machine task counter (used in TaskName)
            machine_task_counter[machine] = machine_task_counter.get(machine, 0) + 1

            # Reset or increment TaskSeqNum
            task_seq_counter = 10 if machine != prev_machine else task_seq_counter + 10
            prev_machine = machine

            # Build TaskName correctly:
            task_name = (
                f"{part_type}_{feature_name}_{machine_task_counter[machine]}"
                if "FinishedPart" not in feature_name
                else f"{part_type}_Finish"
            )

            # Build RandomPro expression (±10%)
            low = round(proc_time * 0.9, 3)
            mode = round(proc_time, 3)
            high = round(proc_time * 1.1, 3)
            random_pro = f"Random.Triangular({low},{mode},{high})"

            # Append row to result list
            result_rows.append({
                'TaskName': task_name,
                'Process': row['Process'],
                'TaskSeqNum': task_seq_counter,
                'Tool': tool,
                'ProcessingTime': proc_time,
                'RandomPro': random_pro
            })

    # Return result as DataFrame
    return pd.DataFrame(result_rows)

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

        # Print result
        print(processing_tasks_df)
