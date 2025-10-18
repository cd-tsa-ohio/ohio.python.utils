import ou_file_utils as ou
import resources as r
import parttable as pt
import feature_selection_module as fsm
import pandas as pd
import partRoutings as pr
import ProcessingTask as ptask
import processes as proc
from parttable import partTable

def makeSimioTables(select_func=fsm.feature_selection_max, pref_mach_list = None, pref_machine - None):

    fs_drs = ou.getFilesDataFrames()

    # === Initialize final dataframes ===
    resFrame = pd.DataFrame()
    taskFrame = pd.DataFrame()
    routing_frame = pd.DataFrame()
    part_routing_clean = pd.DataFrame()
    process_df = pd.DataFrame()

    # === PartTable ===
    part_table_df = partTable(fs_drs.keys())

    # === Loop through all files ===
    for k in fs_drs.keys():
        pn = pt.partName(k)
        df = fs_drs[k]

        # === Feature selection ===
        feat_process = select_func(input_df = df, keywords = pref_mach_list, keyword = pref_machine)

        # === PartRoutings (raw expanded routing) ===
        part_routing = ptask.PartRoutingsWithFullData([k])
        routing_frame = pd.concat([routing_frame, part_routing], ignore_index=True)

        # === Processing Tasks ===
        tasks = ptask.buildProcessingTasksDF(part_routing)
        taskFrame = pd.concat([taskFrame, tasks], ignore_index=True)

        # === Clean PartRoutings from processing tasks ===
        clean_routing = pr.extract_part_routings(tasks)
        part_routing_clean = pd.concat([part_routing_clean, clean_routing], ignore_index=True)

        # === Resources (machine & tools) ===
        res = r.getResources(feat_process)
        resFrame = pd.concat([resFrame, res], ignore_index=True)

    # === Processes ===
    process_df = proc.extract_unique_processes(taskFrame)

    # === Write all outputs to Excel ===
    with pd.ExcelWriter("Simio_Compiled_Output.xlsx") as writer:
        routing_frame.to_excel(writer, sheet_name="RawPartRoutings", index=False)
        taskFrame.to_excel(writer, sheet_name="ProcessingTasks", index=False)
        process_df.to_excel(writer, sheet_name="Processes", index=False)
        part_routing_clean.to_excel(writer, sheet_name="PartRoutings", index=False)
        part_table_df.to_excel(writer, sheet_name="PartTable", index=False)
        resFrame.drop_duplicates(subset=["ResourceName", "ObjectType"]).to_excel(writer, sheet_name="Resources", index=False)

    print("Simio tables exported to Simio_Compiled_Output.xlsx")


# === Run if script is executed directly ===
if __name__ == "__main__":
    # input from user function, pref machine list and pref machine
    func = ""
    pref_mach_list = []
    pref_machine = ""
    makeSimioTables(select_func = func, pref_mach_list = pref_mach_list, pref_machine = pref_machine)
