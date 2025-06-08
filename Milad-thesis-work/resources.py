import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max  # Import the feature selection function

def getResources(DataFrame):
   
   
    resources_data = []

    #duplicates removal step
    seen_resources = set()
       
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
