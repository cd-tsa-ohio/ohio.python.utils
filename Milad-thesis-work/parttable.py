import pandas as pd
import ou_file_utils as ou


def partTable(file_names):

    #number of files calculation
    total_files = len(file_names)

    #Calculate the base part mix
    base_mix = 100 // total_files

    #to distribute remainder in case on unevenness 
    remainder = 100 % total_files
    
    #create a list to store part table data
    part_data =[]

    #iterate through rows in the DataFrame
    for i, file in enumerate(file_names):
        
       #handle tuple or string
        file_path = file[0] if isinstance(file, tuple) else file
       
        new_fn = partName(file_path)
        
        #add 1 to base_mix in case there is a remainder
        part_mix = base_mix + (1 if i < remainder else 0)
        
        part_data.append({
            "ResourceName": new_fn, # file name as the reousrce name
            "EntityType": "ModelEntity",
            "PartMix": part_mix,
            "XLocation": 0,
            "YLocation": 0,
            "Zlocation": 0
            })

    #convert the list to a dataframe
    part_table = pd.DataFrame(part_data)

    return part_table
def partName(file_path):
    new_fn = file_path[file_path.rfind('/') + 1 : file_path.rfind('.')] #adding ". so it can support all type of files"
    return new_fn

if __name__ == "__main__":
    df=ou.getFiles()
    part_table = partTable(df)
    print(part_table)
