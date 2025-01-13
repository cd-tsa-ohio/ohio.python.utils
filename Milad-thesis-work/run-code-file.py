import ou_file_utils as ou
#dfs = ou.getDataFrames()

#for df in dfs:
#   print (df.head())


def makeSimioTables (select_func = feature_selection_max):

    fs_drs = ou.getFilesDataFrames()
    resFrame = pd.DataFrame
    taskFrame = pd.DataFrame

    for k in fs_drs.keys():
        df = fs_drs[k]
        entity = getEntity(k)
        feat_process = select_func(df)
        #resources
     #   resFrame.append(getResources(feature_process))
        # tasks
        # processes
        # routing
        # arrivals
        # parttable

# file.rfind('/')
#39
# file[file.rfind('/'):]


from feature_selection_module import feature_selection_max, feature_selection_min, feature_selection_median #import all three functions from the feature_selection_module

# Load DataFrames using ou_file_utils
dfs = ou.getDataFrames()

# Process each DataFrame using the imported functions
for file_info in dfs:
    file_name = file_info['file_name']  # Extract file name
    df = file_info['data']             # Extract DataFrame
    print(f"Processing file: {file_name}\n")

    # Maximum processing time
    max_df = feature_selection_max(df)
    print(f"Features with Maximum Processing Time for DataFrame {file_name}\n:")
    print(max_df, "\n")
    
    # Minimum processing time
    min_df = feature_selection_min(df)
    print(f"Features with Minimum Processing Time for DataFrame {file_name}\n:")
    print(min_df, "\n")
    
    # Median processing time
    median_df = feature_selection_median(df)
    print(f"Features with Median Processing Time for DataFrame {file_name}\n:")
    print(median_df, "\n")
