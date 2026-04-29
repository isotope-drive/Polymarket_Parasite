import pandas as pd
import json
from collector import BASE_PATH

with open(f"{BASE_PATH}/tests/trades.json") as f:
    raw = json.load(f)  

rows = []
for event_id, trades in enumerate(raw):
    for trade_idx, trade in enumerate(trades):
        rows.append({"event_id": event_id, "trade_index": trade_idx, **trade})

df = pd.DataFrame(rows)

print(df.head())
print(df.memory_usage())

df.to_parquet(path=f"{BASE_PATH}/data/dataframe.parquet")