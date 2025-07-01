import os
from dotenv import load_dotenv
import pandas as pd
import ou_file_utils as ou
from feature_selection_module import feature_selection_max

load_dotenv()

def lookup_coordinates(object_type: str, resource_name: str):
    """
    Returns (x, y, z, capacity) as floats/ints from .env or defaults.
    """
    key = f"{object_type.upper()}_{resource_name}".upper().replace(" ", "_")
    
    # If not found, fallback to RESOURCE_DEFAULT or generic default
    loc = os.getenv(key)
    if not loc and object_type == "Resource":
        loc = os.getenv("RESOURCE_DEFAULT")
    
    if loc:
        try:
            x, y, z, cap = map(float, loc.split(","))
            return x, y, z, int(cap)
        except ValueError:
            pass
    
    # Fallback if nothing found or malformed
    return 0.0, 0.0, 0.0, 1

def getResources(DataFrame):
    resources_data = []
    seen_resources = set()

    for _, row in DataFrame.iterrows():
        # Machines
        machine_name = row["Machine"]
        if (machine_name, "Machine") not in seen_resources:
            x, y, z, cap = lookup_coordinates("Machine", machine_name)

            # Derive ObjectType from machine_name (strip 'Cnc' if present)
            object_type = machine_name[3:] if machine_name.lower().startswith("cnc") else machine_name

            resources_data.append({
                "ResourceName": machine_name,
                "ObjectType": object_type,
                "XLocation": x,
                "YLocation": y,
                "ZLocation": z,
                "InitialCapacity": cap
            })
            seen_resources.add((machine_name, "Machine"))

    for _, row in DataFrame.iterrows():
        # Tools
        tool_name = row["Tool"]
        if (tool_name, "Resource") not in seen_resources:
            x, y, z, cap = lookup_coordinates("Resource", tool_name)

            # Tools use a fixed ObjectType
            object_type = "Tool"

            resources_data.append({
                "ResourceName": tool_name,
                "ObjectType": object_type,
                "XLocation": x,
                "YLocation": y,
                "ZLocation": z,
                "InitialCapacity": cap
            })
            seen_resources.add((tool_name, "Resource"))

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
