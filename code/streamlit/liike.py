import duckdb as dd
import gigafunctions as giga
import pandas as pd

def read_node(tbl: str, node:str, file:str):
    con = dd.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node}").fetchdf()
    con.close()
    return df
file = "../data/duckdb.database"
tbl = "Silver_SensorData"
node = "3200"
df = read_node(tbl, node, file)

def count_paths_monthly(df):
    # Muuntaa timestamp-sarakkeen datetime-tyyppiseksi ja asettaa sen indeksiksi
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # Laskee asiakasmäärät eri kuukausille käyttäen giga.count_paths-funktiota
    monthly_counts = df.resample('ME').apply(lambda x: giga.count_paths(x))
    
    return monthly_counts

monthly_counts = count_paths_monthly(df)
print(monthly_counts)