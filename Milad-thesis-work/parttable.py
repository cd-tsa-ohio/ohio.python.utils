import pandas as pd
import ou_file_utils as ou


def partTable(DataFrame):

    #create a list to store part table data
    part_data =[]

    #iterate through rows in the DataFrame
    for index, row in DataFrame.iterrows():
        part_data.append({
            "ResourceName": "file_name", # file name as the reousrce name
            "EntityType": "ModelEntity",
            "PartMix": 1.0,
            "XLocation": 0,
            "YLocation": 0,
            "Zlocation": 0
        })

    #convert the list to a dataframe
    part_table = pd.DataFrame(part_data)

    return part_table

if __name__ == "__main__":
    df=ou.getDataFrame()
    part_table = partTable(df)
    print(part_table)