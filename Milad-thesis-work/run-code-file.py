import ou_file_utils as ou
import resources as r
from parttable import partTable
import feature_selection_module as fsm
import pandas as pd
import partRoutings as pr
import parttable as pt
#dfs = ou.getDataFrames()

#for df in dfs:
#   print (df.head())


def makeSimioTables (select_func = fsm.feature_selection_max):

    fs_drs = ou.getFilesDataFrames()
    resFrame = pd.DataFrame
    taskFrame = pd.DataFrame
    routing_frame =pd.DataFrame
    part_table_df = partTable(fs_drs.keys())
    for k in fs_drs.keys():
        pn = pt.partName(k)
        df = fs_drs[k]
    #entity = getEntity(k)
        feat_process = select_func(df)
        routing_frame.concat(pr.PartRoutings(pn,df))
        #resources
        resFrame.concat(r.getResources(feat_process))
        # tasks
        # processes
        # routing
        # arrivals
        # parttable

if __name__ == "__main__":
    makeSimioTables()



