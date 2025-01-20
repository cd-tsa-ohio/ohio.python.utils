import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max  # Import the feature selection function

def getResources(DataFrame):
   
    # Step 1: Prompt user to select files using ou.getFiles()
  #  selected_files = ou.getFiles()

    # Step 2: Load the selected files into DataFrames
   # fs_drs = ou.getFilesDataFrames()

    # Step 3: Prepare a list to accumulate rows for the resources table
    resources_data = []

    # Step 4: Iterate through the files and create the resources table
   # for file_name, df in fs_drs.items():
        # Apply the feature selection function passed as a parameter
   #     filtered_df = select_func(df)
    #duplicates removal step
    seen_resources = set()
        # Step 5: Extract machines and tools for ResourceName
    for index, row in DataFrame.iterrows():
            # Add machine as a resource if not already added
        if (row["Machine"], "Machine") not in seen_resources:
            resources_data.append({
                "ResourceName": row["Machine"],  # Assuming 'Machines' is in the filtered DataFrame
                "ObjectType": "Machine",  # Keep 'Machine' for machines
                "XLocation": 0,  # Default X location
                "YLocation": 0,  # Default Y location
                "ZLocation": 0,  # Default Z location
                "InitialCapacity": 1  # Default initial capacity
            })
            seen_resources.add((row["Machine"], "Machine"))
        
        
        # Add tool as a resource if not already added
        if (row["Tool"], "Tool") not in seen_resources:
            resources_data.append({
                "ResourceName": row["Tool"],  # Assuming 'tools' is in the filtered DataFrame
                "ObjectType": "Resources",  # Use 'Resources' for tools
                "XLocation": 0,  # Default X location
                "YLocation": 0,  # Default Y location
                "ZLocation": 0,  # Default Z location
                "InitialCapacity": 1  # Default initial capacity
                })
            seen_resources.add((row["Tool"], "Tool"))

    # Step 6: Convert the list of dictionaries to a DataFrame
    resources_table = pd.DataFrame(resources_data)

    return resources_table

if __name__ == "__main__":
    df=ou.getDataFrame()
    resources_table = getResources(df)
    print(resources_table)