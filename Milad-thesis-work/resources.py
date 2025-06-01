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
        
    for index, row in DataFrame.iterrows(): 
        # Add tool as a resource if not already added
        if (row["Tool"], "Resource") not in seen_resources:
            resources_data.append({
                "ResourceName": row["Tool"],  # Assuming 'tools' is in the filtered DataFrame
                "ObjectType": "Resource",  # Use 'Resources' for tools
                "XLocation": 0,  # Default X location
                "YLocation": 0,  # Default Y location
                "ZLocation": 0,  # Default Z location
                "InitialCapacity": 1  # Default initial capacity
                })
            seen_resources.add((row["Tool"], "Resource"))

    return pd.DataFrame(resources_data)

    # Step 6: Convert the list of dictionaries to a DataFrame
    #resources_table = pd.DataFrame(resources_data)

    #return resources_table

#make another function getallResources which will take list of dataframes

def getAllResources(dataframes_list):
    all_resources = pd.DataFrame()
    for df in dataframes_list:
        table = getResources(df)
        all_resources = pd.concat([all_resources, table], ignore_index=True)
    return all_resources.drop_duplicates(subset=["ResourceName", "ObjectType"])


if __name__ == "__main__": #get in a loop 
    dataframes_list = ou.getDataFrames()  # list of DataFrames
    resources_table = getAllResources(dataframes_list)
    print(resources_table)
    
    
    #df=ou.getDataFrames() # add get dataframes() for multiple files and test try
    #resources_table = getResources(df)
    #print(resources_table)