#duckdb etl
import duckdb
import duck_reader
from pathlib import Path


#iterates over csv files in projekti1 dir
str_dir = '../data/projekti1/'

pathlist = Path(str_dir).glob('*.csv')
for path in pathlist:
    path_in_str = str(path)   
    print(path_in_str)


#korjataan z-arvot ja ms pois datasta
