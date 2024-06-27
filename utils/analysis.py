import pandas as pd
from ydata_quality.duplicates import DuplicateChecker
from ydata_quality.missings import MissingsProfiler

def duplicate_checker(df):
    dc = DuplicateChecker(df=df)
    results = dc.evaluate()
    return results

def missing_checker(df):
    mp = MissingsProfiler(df=df, random_state=42)
    results = mp.evaluate()
    r = list(results.items())
    r.insert(0, ('null_count', mp.null_count().to_dict())) 
    return dict(r)

def combine_analysis(missing_values, duplicate_values):
    combined_dict = {
        "missing_values": missing_values,
        "duplicate_values": duplicate_values
    }
    return combined_dict
