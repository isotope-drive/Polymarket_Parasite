import collector
import tidy_data
import parquet_manager


collector.controller("trades")	#fetch trades
parquet_manager.to_parquet("trades")	#json to parquet #only run once
parquet_manager.read_parquet_df("trades")	#parquet back to df
