import pandas as pd 
import matplotlib.pyplot as plt 
import os
import parquet_manager
from collector import BASE_PATH



def clean_columns(df : pd.DataFrame):
	print("\nCleaning Columns\n")

	before_memory = df.memory_usage().sum()

	df = df.drop(columns = ['icon','bio','profileImage','profileImageOptimized'])
    
	after_memory = df.memory_usage().sum()

	delta = before_memory-after_memory

	print(f"Original: {before_memory/1_000_000}Mb\n"
	f"Cleaned: {after_memory/1_000_000}Mb\n"
	f"Delta: {delta/1_000_000}Mb\n")

	return df


    
