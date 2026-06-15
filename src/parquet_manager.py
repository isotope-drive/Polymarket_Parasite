import pandas as pd
import json
import os
from collector import BASE_PATH


def to_parquet(file_name: str):
    with open (f"{BASE_PATH}/data/{os.path.splitext(file_name)[0]}.json") as f:
        raw = json.load(f)

    rows = []
    for event_id, trades in enumerate(raw):
        for trade_idx, trade in enumerate(trades):
            rows.append({"event_id": event_id, "trade_index": trade_idx, **trade})

    df = pd.DataFrame(rows)

    print(df.head())
    print(df.memory_usage())

    df.to_parquet(path=f"{BASE_PATH}/data/{os.path.splitext(file_name)[0]}.parquet")



def read_parquet_df(file_name: str):
    file_name_list = os.path.splitext(file_name)

    return pd.read_parquet(f"{BASE_PATH}/data/{file_name_list[0]}.parquet")