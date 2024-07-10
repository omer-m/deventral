import pandas as pd
from .profiling_strategy import DataProfilingStrategy, YDataProfilingStrategy
import json


class DataProfiler:
    def __init__(self, strategy: DataProfilingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DataProfilingStrategy):
        self._strategy = strategy

    def profile_data(self, data):
        return self._strategy.generate_profile(data)

def analysis_report(df):
    profiler = DataProfiler(YDataProfilingStrategy())  # Use the YDataProfilingStrategy by default
    profile = profiler.profile_data(df)
    report = json.loads(profile.to_json())
    
    
    # List of main keys to extract
    keys_to_extract = ["table", "variables", "correlations", "alerts", "duplicates"]

    # List of sub-keys within "variables"
    variable_sub_keys = [
        "n_distinct", "p_distinct", "is_unique", "n_unique", "p_unique", "type", "value_counts_without_nan",
        "n_missing", "n", "p_missing", "count", "imbalance", "n_negative", "p_negative", "n_infinite",
        "n_zeros", "mean", "std", "variance", "min", "max", "kurtosis", "skewness", "sum", "mad", "range",
        "5%", "25%", "50%", "75%", "95%", "iqr", "cv", "p_zeros", "p_infinite", "chi_squared", "word_counts",
        "block_alias_counts"
    ]

    # Extracting the selected keys and their values
    extracted_data = {key: report[key] for key in keys_to_extract if key in report}

    # Extracting specific sub-keys for each variable in "variables"
    if "variables" in extracted_data:
        extracted_data["variables"] = {
            var_key: {sub_key: var_value[sub_key] for sub_key in variable_sub_keys if sub_key in var_value}
            for var_key, var_value in report["variables"].items()
        }
    # Extracting data from the JSON object
    variables = extracted_data.get("variables", {})
    table_stats = extracted_data.get("table", {})

    # Get the required table-level metrics
    table_metrics = {
        "p_cells_missing": table_stats.get("p_cells_missing"),
        "p_duplicates": table_stats.get("p_duplicates")
    }

    # Initialize a dictionary to store the variable-level metrics
    variable_metrics = {}

    # Extract the required metrics for each variable
    for var_name, var in variables.items():
        variable_metrics[var_name] = {
            "p_distinct": var.get("p_distinct"),
            "p_unique": var.get("p_unique"),
            "p_missing": var.get("p_missing"),
            "iqr": var.get("iqr")
        }

    # Combine table-level and variable-level metrics
    kpi = {
        "table_metrics": table_metrics,
        "variable_metrics": variable_metrics
    }

    return extracted_data,kpi