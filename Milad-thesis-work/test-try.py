import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max  # Import the feature selection function

def createResourcesTable(select_func=feature_selection_max):
   
    # Step 1: Prompt user to select files using ou.getFiles()
  #  selected_files = ou.getFiles()

    # Step 2: Load the selected files into DataFrames
    fs_drs = ou.getFilesDataFrames()

    # Step 3: Prepare a list to accumulate rows for the resources table
    resources_data = []

    # Step 4: Iterate through the files and create the resources table
    for file_name, df in fs_drs.items():
        # Apply the feature selection function passed as a parameter
        filtered_df = select_func(df)

        # Step 5: Extract machines and tools for ResourceName
        for index, row in filtered_df.iterrows():
            # Add machine as a resource
            resources_data.append({
                "ResourceName": row["Machine"],  # Assuming 'Machines' is in the filtered DataFrame
                "ObjectType": "Machine",  # Keep 'Machine' for machines
                "XLocation": 0,  # Default X location
                "YLocation": 0,  # Default Y location
                "ZLocation": 0,  # Default Z location
                "InitialCapacity": 1  # Default initial capacity
            })

            # Add tool as a resource
            resources_data.append({
                "ResourceName": row["Tool"],  # Assuming 'tools' is in the filtered DataFrame
                "ObjectType": "Resources",  # Use 'Resources' for tools
                "XLocation": 0,  # Default X location
                "YLocation": 0,  # Default Y location
                "ZLocation": 0,  # Default Z location
                "InitialCapacity": 1  # Default initial capacity
            })

    # Step 6: Convert the list of dictionaries to a DataFrame
    resources_table = pd.DataFrame(resources_data)

    return resources_table

if __name__ == "__main__":
    resources_table = createResourcesTable()
    print(resources_table)