import pandas as pd
import duckdb as dd


file = "../data/duckdb.database"


def read_node(tbl: str, node_name: str):
    '''
    Hakee kaikki noden rivit

    Args:
        tbl (str): Taulun nimi 
        node_name (str): Noden nimi

    Returns:
        pandas.DataFrame: Noden rivit
    '''
    con = dd.connect(database=file)
    df = con.sql(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").df()
    con.close()
    return df