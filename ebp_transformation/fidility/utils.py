import pandas as pd

def normalize(s):
    # lower, strip, and remove non-breaking spaces etc.
    return str(s).strip().lower()


def get_header_row(input_path, expected_headers: list) -> int:
    try:
        df_raw =  pd.read_excel(input_path, header=None)
    except Exception:
        try:
            df_raw =  pd.read_csv(input_path, header=None)
        except Exception as e:
            raise ValueError(f"Unsupported file format or corrupted file: {input_path}")
    
    headers = [normalize(h) for h in expected_headers]
    header_row = None
    for i, row in df_raw.iterrows():
        row_vals = [normalize(v) for v in row.tolist() if pd.notna(v)]
        # check that all expected headers are present in this row (subset)
        if set(headers).issubset(set(row_vals)):
            header_row = i
            break
    
    return header_row


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