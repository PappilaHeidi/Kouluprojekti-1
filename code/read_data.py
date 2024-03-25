import pandas as pd
import os
import glob
from datetime import datetime, date, time

def read_csv_raw(filename):
    print("handling", filename)
    df = pd.read_csv(filename, 
                  sep=",", 
                  header=0,
                  index_col=['timestamp'],
                  parse_dates=['timestamp']
)
    print("found", df.size, "lines")
    return df
