import os
import pandas as pd
import random
import ou_file_utils as ou
from feature_selection_module import feature_selection_max
alternate = 'a'

# === Helper function: extract part name from file path ===
def partName(file_path):
    return file_path[file_path.rfind('/') + 1 : file_path.rfind('.')]

# === Build Part Routings DataFrame with required columns ===
def PartRoutingsWithFullData(file_names, select_func, kwargs):
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
#            df = feature_selection_max(df).copy()
            df = select_func (**kwargs).copy()

            # Add PartType and PartDestinationID columns
            df['PartType'] = name
            df['PartDestinationID'] = df.groupby('Machine').cumcount() + 1

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

    for part_type, group in part_routings_df.groupby('PartType'):
        machine_indices = {}  # (machine_name) → index (starts from 1)
        task_counts = {}      # (machine_index) → task counter

        for _, row in group.iterrows():
            feature = row['Feature Name']
            machine = row['Machine'].replace("Input@", "")  # Clean machine name
            tool = row['Tool']
            proc_time = row['Processing Time']

            # Assign or reuse machine index
            if machine not in machine_indices:
                machine_indices[machine] = len(machine_indices) + 1
            machine_index = machine_indices[machine]

            # Task counter per machine index
            key = (part_type, machine_index)
            task_counts[key] = task_counts.get(key, 0) + 1
            task_number = task_counts[key]

            # TaskSeqNum: 10 * task_number
            task_seq_num = 10 * task_number

            # TaskName logic
            if "FinishedPart" not in feature:
                task_name = f"{part_type}_{machine_index}{alternate}_{feature}_{task_number}"
                process_name = f"{part_type}_{machine_index}{alternate}_{machine}"
            else:
                task_name = f"{part_type}_Finish"
                process_name = f"{part_type}_Complete"
                task_seq_num = 10  # Always 10 for finish

            # Build RandomPro
            low = round(proc_time * 0.9, 3)
            mode = round(proc_time, 3)
            high = round(proc_time * 1.1, 3)
            random_pro = f"Random.Triangular({low},{mode},{high})"

            result_rows.append({
                'TaskName': task_name,
                'Process': process_name,
                'TaskSeqNum': task_seq_num,
                'Tool': tool,
                'ProcessingTime': proc_time,
                'RandomPro': random_pro
            })

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
