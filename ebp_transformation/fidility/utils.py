import pandas as pd

def drop_ending_rows(df: pd.DataFrame) -> pd.DataFrame:
    header_len = len(df.columns)

    stop_index = len(df)
    blank_found = False

    for i, row in df.iterrows():
        if row.isna().all():
            blank_found = True
            continue

        if blank_found:
            if row.count() != header_len:  # mismatch
                stop_index = i
                break
    
    updated_df = df.iloc[:stop_index]
    return updated_df