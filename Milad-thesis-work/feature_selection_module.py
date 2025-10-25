import pandas as pd
import ou_file_utils as ou


def feature_selection_max(input_df):
    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in input_df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and select the row with maximum 'Processing Time' for each group
        max_processing_time_df = input_df.loc[input_df.groupby('Feature Name')['Processing Time'].idxmax()]

        # Reset index for a clean output DataFrame
        max_processing_time_df = max_processing_time_df.reset_index(drop=True)
        
        return max_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def feature_selection_min(input_df):
   
    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in input_df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and select the row with minimum 'Processing Time' for each group
        min_processing_time_df = input_df.loc[input_df.groupby('Feature Name')['Processing Time'].idxmin()]

        # Reset index for a clean output DataFrame
        min_processing_time_df = min_processing_time_df.reset_index(drop=True)
        
        return min_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
def feature_selection_median(df):

    try:
        # Validate required columns
        required_columns = ['Feature Name', 'Processing Time']
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")

        # Group by 'Feature Name' and calculate the median processing time
        median_processing_time_df = df.groupby('Feature Name', as_index=False)['Processing Time'].median()

        # Rename the column for clarity
        median_processing_time_df.rename(columns={'Processing Time': 'Median Processing Time'}, inplace=True)
        
        return median_processing_time_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error



#Implementing test functions to pick only slow and fast machines for feature selection module


def feature_selection_max_PT(
    input_df: pd.DataFrame,
    feature_col: str = "Feature Name",
    time_col: str = "Processing Time",
    machine_col: str | None = None,
    keyword: str = "Slow",
    case_sensitive: bool = False,
) -> pd.DataFrame:
    """
    One row per feature:
      1) If any machine name contains `keyword`, pick the max(time) among those.
      2) Otherwise, pick the max(time) in the whole feature group.
    Auto-detects the machine column if not provided.
    """
    if feature_col not in input_df.columns or time_col not in input_df.columns:
        raise ValueError(f"Missing required columns: {[c for c in (feature_col, time_col) if c not in input_df.columns]}")

    # Auto-detect machine column
    if machine_col is None:
        for cand in ("Machine Name", "Machine"):
            if cand in input_df.columns:
                machine_col = cand
                break
        if machine_col is None:
            raise ValueError("Could not find a machine column. Expected 'Machine Name' or 'Machine'.")

    df = input_df.copy()
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")

    picks = []
    for _, g in df.groupby(feature_col, sort=False, dropna=False):
        g = g.dropna(subset=[time_col])
        if g.empty:
            continue

        # pool 1: machines containing keyword
        mask = g[machine_col].astype(str).str.contains(keyword, case=case_sensitive, na=False)
        pool = g[mask] if mask.any() else g

        # pick: row with max processing time (ties -> first occurrence)
        idx = pool[time_col].idxmax()
        picks.append(idx)

    return input_df.loc[picks].reset_index(drop=True)



def feature_selection_min_PT(
    input_df: pd.DataFrame,
    feature_col: str = "Feature Name",
    time_col: str = "Processing Time",
    machine_col: str | None = None,
    keyword: str = "Fast",
    case_sensitive: bool = False,
) -> pd.DataFrame:
    """
    One row per feature:
      1) If any machine name contains `keyword`, pick the min(time) among those.
      2) Otherwise, pick the min(time) in the whole feature group.
    Auto-detects the machine column if not provided.
    """
    if feature_col not in input_df.columns or time_col not in input_df.columns:
        raise ValueError(f"Missing required columns: {[c for c in (feature_col, time_col) if c not in input_df.columns]}")

    # Auto-detect machine column
    if machine_col is None:
        for cand in ("Machine Name", "Machine"):
            if cand in input_df.columns:
                machine_col = cand
                break
        if machine_col is None:
            raise ValueError("Could not find a machine column. Expected 'Machine Name' or 'Machine'.")

    df = input_df.copy()
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")

    picks = []
    currIdx =0
    keywords = []
    for _, g in df.groupby(feature_col, sort=False, dropna=False):
        g = g.dropna(subset=[time_col])
        if g.empty:
            continue
        
        key = keywords [(currIdx + 1) % keywords.size()]

# pool 1: machines containing keyword
        mask = g[machine_col].astype(str).str.contains(keyword, case=case_sensitive, na=False)
        pool = g[mask] if mask.any() else g

        # pick: row with max processing time (ties -> first occurrence)
        idx = pool[time_col].idxmin()
        picks.append(idx)

    return input_df.loc[picks].reset_index(drop=True)




#test try of the logic for rotating amongst the machines

def feature_selection_mach_pref_spt(
    input_df: pd.DataFrame,
    feature_col: str = "Feature Name",
    time_col: str = "Processing Time",
    machine_col: str | None = None,     # auto-detects if None
    keyword: str = "Fast",              # single-keyword fallback
    keywords: list[str] | None = None,  # rotation list e.g. ["4axisMillFast","HMillFast","VMillFast"]
    case_sensitive: bool = False,
) -> pd.DataFrame:
    """
    One row per feature:
      • Try rotating keywords across features (i-th feature starts with keywords[i % len]).
      • If none match, try single `keyword`.
      • If none match, pick overall min(time).
    """
    if feature_col not in input_df.columns or time_col not in input_df.columns:
        miss = [c for c in (feature_col, time_col) if c not in input_df.columns]
        raise ValueError(f"Missing required columns: {miss}")

    if machine_col is None:
        for cand in ("Machine Name", "Machine"):
            if cand in input_df.columns:
                machine_col = cand
                break
        if machine_col is None:
            raise ValueError("Could not find a machine column. Expected 'Machine Name' or 'Machine'.")

    df = input_df.copy()
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")

    picks = []
    groups = list(df.groupby(feature_col, sort=False, dropna=False))

    for i, (_, g) in enumerate(groups):
        g = g.dropna(subset=[time_col])
        if g.empty:
            continue

        chosen_idx = None

        # Rotate across provided keywords
        if keywords:
            K = len(keywords)
            for step in range(K):
                kw = keywords[(i + step) % K]
                mask = g[machine_col].astype(str).str.contains(kw, case=case_sensitive, na=False)
                if mask.any():
                    chosen_idx = g.loc[mask, time_col].idxmin()
                    break

        # Single-keyword fallback (e.g., "Fast")
        if chosen_idx is None and keyword:
            mask = g[machine_col].astype(str).str.contains(keyword, case=case_sensitive, na=False)
            if mask.any():
                chosen_idx = g.loc[mask, time_col].idxmin()

        # Final fallback: overall min
        if chosen_idx is None:
            chosen_idx = g[time_col].idxmin()

        picks.append(chosen_idx)

    return input_df.loc[picks].reset_index(drop=True)



#running the functions to make sure they give correct answer and dataframe format

if __name__ == "__main__":
    
    # Get your data
    try:
        df = ou.getDataFrames()
    except NameError:
        df = ou.getDataFrames()

    # Handle if df is a list of DataFrames
    if isinstance(df, list):
        df = df[0] if df else pd.DataFrame()

    # Show the actual columns
    print("Input columns:", df.columns.tolist())

    # Rotate among specific FAST machines first; then fallback to generic "Fast"; then overall min
    fast_keywords = ["4axisMillFast", "HMillFast", "VMillFast"]

    result = feature_selection_mach_pref_spt(
        df,
        keywords=fast_keywords,   # rotation across these
        keyword="Fast",           # single-keyword fallback
        case_sensitive=False
    )

    print("Filtered DataFrame:")
    print(result)


#if __name__ == "__main__":
   # df = ou.getDataFrames()
    
    # Handle if df is a list of DataFrames
   # if isinstance(df, list):
  #      df = df[0] if df else pd.DataFrame()
    
    # Show the actual columns
  #  print("Input columns:", df.columns.tolist())
    
    # Run feature selection
  #  max_processing_time_df = feature_selection_max_slow_first(df, keyword = "VMillFast")
  #  max_processing_time_df = feature_selection_min_fast_first(df, keyword = "HMillFast")
  #  print("Filtered DataFrame:")
  #  print(max_processing_time_df)
