import ou_file_utils as ou
import resources as r
import parttable as pt
import feature_selection_module as fsm
import pandas as pd
import partRoutings as pr
import ProcessingTask as ptask
import processes as proc
from parttable import partTable
import argparse
import os
import inspect


import os, inspect
import pandas as pd

def makeSimioTables(select_func, pref_mach_list=None, pref_machine=None, output_path=None):
    if select_func is None:
        raise ValueError("select_func is required")
    if not output_path:
        raise ValueError("output_path is required")

    fs_drs = ou.getFilesDataFrames()

    # --- final tables (RawPartRoutings removed) ---
    resFrame = pd.DataFrame()
    taskFrame = pd.DataFrame()
    part_routing_clean = pd.DataFrame()   # <-- keep PartRoutings
    part_table_df = partTable(list(fs_drs.keys()))

    sel_params = inspect.signature(select_func).parameters

    for k, df in fs_drs.items():
        # feature selection (for Resources)
        call_kwargs = {"input_df": df}
        if "keywords" in sel_params and pref_mach_list is not None:
            call_kwargs["keywords"] = pref_mach_list
        if "keyword" in sel_params and pref_machine is not None:
            call_kwargs["keyword"] = pref_machine
        feat_process = select_func(**call_kwargs)

        # build tasks from temporary routing (not saved as a sheet)
        part_routing_tmp = ptask.PartRoutingsWithFullData([k])
        tasks = ptask.buildProcessingTasksDF(part_routing_tmp)
        taskFrame = pd.concat([taskFrame, tasks], ignore_index=True)

        # PartRoutings sheet (derived/cleaned from tasks)
        clean_routing = pr.extract_part_routings(tasks)
        part_routing_clean = pd.concat([part_routing_clean, clean_routing], ignore_index=True)

        # resources from selected features
        res = r.getResources(feat_process)
        resFrame = pd.concat([resFrame, res], ignore_index=True)

    # processes from tasks
    process_df = proc.extract_unique_processes(taskFrame)

    # write outputs (NO RawPartRoutings)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        taskFrame.to_excel(writer, sheet_name="ProcessingTasks", index=False)
        process_df.to_excel(writer, sheet_name="Processes", index=False)
        part_routing_clean.to_excel(writer, sheet_name="PartRoutings", index=False)   # <-- kept
        part_table_df.to_excel(writer, sheet_name="PartTable", index=False)

        res_out = resFrame
        if {"ResourceName", "ObjectType"}.issubset(res_out.columns):
            res_out = res_out.drop_duplicates(subset=["ResourceName", "ObjectType"])
        res_out.to_excel(writer, sheet_name="Resources", index=False)

    # summary
    print(f"✔ ProcessingTasks:   {len(taskFrame)} rows")
    print(f"✔ Processes:         {len(process_df)} rows")
    print(f"✔ PartRoutings:      {len(part_routing_clean)} rows")
    print(f"✔ PartTable:         {len(part_table_df)} rows")
    print(f"✔ Resources:         {len(res_out)} rows")
    print("Simio tables exported to:", os.path.abspath(output_path))



# === Run if script is executed directly ===
if __name__ == "__main__":
    import argparse, re, os
    import feature_selection_module as fsm

    # --- helpers ---
    def discover_selectors():
        return sorted(n for n in dir(fsm)
                      if n.startswith("feature_selection_") and callable(getattr(fsm, n)))

    def build_menu(func_names):
        print("Available selection functions:")
        for i, name in enumerate(func_names, start=1):
            print(f"  {i}. {name}")

    parser = argparse.ArgumentParser(description="Build Simio Excel from CSVs using a numbered selection function.")
    parser.add_argument("--funcs", nargs="*", default=None,
                        help="Space-separated list of function names for the menu. "
                             "If omitted, auto-discovers feature_selection_* from feature_selection_module.")
    parser.add_argument("--sel", type=int, default=None,
                        help="Menu number of the function to run (1-based). If omitted, you’ll be prompted.")
    parser.add_argument("--pref-mach-list", nargs="*", default=None,
                        help="Space-separated preferred machine keywords (rotation). e.g. 4axisMillFast HMillFast VMillFast Fast")
    parser.add_argument("--pref-mach", default=None,
                        help='Single fallback keyword (e.g. "Fast" or "Slow")')
    parser.add_argument("--output", default=None,
                        help="Override output Excel path. If omitted, uses <function_name>.xlsx")
    args = parser.parse_args()

    func_names = args.funcs if args.funcs else discover_selectors()
    if not func_names:
        print("No selection functions found.")
        raise SystemExit(2)

    if args.sel is None:
        build_menu(func_names)
        try:
            choice = int(input("Enter the number of the function to run: ").strip())
        except Exception:
            print("Invalid input.")
            raise SystemExit(2)
    else:
        choice = args.sel

    if not (1 <= choice <= len(func_names)):
        print(f"Invalid choice: {choice}. Must be 1..{len(func_names)}.")
        raise SystemExit(2)

    func_name = func_names[choice - 1]
    select_func = getattr(fsm, func_name, None)
    if not callable(select_func):
        print(f"Selected function '{func_name}' is not callable/found.")
        raise SystemExit(2)

    if args.pref_mach_list is None:
        raw = input("Enter space-separated preferred machines (or press Enter to skip): ").strip()
        args.pref_mach_list = raw.split() if raw else None

    if args.pref_mach is None:
        raw = input('Enter single fallback keyword (e.g., "Fast" or "Slow"; press Enter to skip): ').strip()
        args.pref_mach = raw or None

    # Auto output name from function if not provided
    safe_base = re.sub(r"[^A-Za-z0-9._-]+", "_", func_name)
    output_path = args.output or f"{safe_base}.xlsx"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    print(f"Using selector: {func_name}")
    if args.pref_mach_list: print(f"Rotating keywords: {args.pref_mach_list}")
    if args.pref_mach:      print(f"Single fallback keyword: {args.pref_mach}")
    print(f"Output: {output_path}")

    makeSimioTables(
        select_func=select_func,
        pref_mach_list=args.pref_mach_list,
        pref_machine=args.pref_mach,
        output_path=output_path,
    )

