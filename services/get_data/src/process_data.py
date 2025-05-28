import pandas as pd
from loguru import logger
import time
import json


def remove_empty_values(
      result: list[dict]  
    ) -> list[dict]:

        # declare output list
    new_result_list = []

    start_cleaning_time = time.time()
    
    # Iterate over the current result
    for row in result:
        cleaned_row = {}
        for key, value in row.items():
            # Skip @odata.type metadata fields and fields with dots
            if ("@" in key) or ("." in key):
                continue
            # Handle empty dict
            elif value == {}:
                cleaned_row[key] = None
            elif isinstance(value, dict):
                cleaned_row[key] = json.dumps(value)
            # Handle lists (both empty and non-empty)
            elif isinstance(value, list):
                if len(value) == 0:
                    cleaned_row[key] = None
                else:
                    # Convert non-empty lists to JSON string for SQL Server
                    cleaned_row[key] = json.dumps(value)
            # Handle None values
            elif value is None:
                cleaned_row[key] = None
            # Convert all numeric values to consistent types
            elif isinstance(value, (int, float)):
                # Convert to float for consistency (Polars can handle this better)
                cleaned_row[key] = float(value) if value is not None else None    
            else:
                cleaned_row[key] = value
        
        new_result_list.append(cleaned_row)
                
    end_cleaning_time = time.time()
    time_cleaning = end_cleaning_time - start_cleaning_time                
    logger.info(f"Removing empty value took {time_cleaning:.2f} seconds for {len(result)} rows")

    return new_result_list

def process_result(
        result: list[dict]
    ):
    """"
    Replace {} values in columns by None, it is due to polars cand handle this cases, and it needs to be modify
    """

    # Remove empty values
    new_result_list = remove_empty_values(result)

    return new_result_list