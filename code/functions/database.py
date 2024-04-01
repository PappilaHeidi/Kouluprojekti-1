import duckdb
import pandas as pd
import os
import time

def table_exists(conn, table_name):
    """
     Apufunktio, jonka avulla voidaan tarkastaa onko haluttu DuckDB taulu olemassa vai ei.
    """
    try:
        conn.execute(f"SELECT * FROM {table_name} LIMIT 1")
        return True
    except duckdb.Error:
        return False
    
def create_db_table(table_name, database, schema):
    """
     Apufunktio, jonka avulla luodaan tietokantataulu halutulla schemalla.
    Inputs:
        table_name(str): Tietokantataulun nimi
        database(str): Pathi database tiedostoon
        schema(str): Tietokantataulun luonti sql schema (create table yms.)
    """
    conn = duckdb.connect(database=database, read_only=False)
    if not table_exists(conn=conn, table_name=table_name):
        conn.execute(schema)
        print(f"{table_name} luotu")
    else:
        print(f"{table_name} on jo olemassa")

def insert_csv_files_into_table(csv_folder, table_name, db_file, lite):
    """
    Inputs:
        csv_folder(str): Kansion path, jossa on kaikki csv-tiedostot
        table_name(str): Tietokantataulun nimi DuckDB:ssä, johon tiedostot tallennetaan
        db_file(str): Tietokanta tiedoston path, jossa sijaitsee duckdb tietokanta
        connection(duckdb.connect()): DuckDB Connection methodi
        lite(Boolean): True/False, ajetaanko tietokantaan kevennetty "Lite"-versio vai koko datasetti.
    """
    start_time = time.time()  # Alustetaan ajastin, jonka avulla voidaan seurata koodin etenemistä
    files_processed = 0  # Kuinka monta tiedostoa on prosessoitu
    lite_file = "node_3200.csv" # Valitse mitä tiedostoa käytetetään kevennetyssä tietokannassa.
    csv_count = 0

    # Lasketaan montako csv-tiedostoa meillä on
    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            csv_count += 1
    
    conn = duckdb.connect(database=db_file, read_only=False)
    if not lite: #Ajetaan koko kanta
        # Otetaan lista kaikista CSV-tiedostoista ja luodaan FOR-loop, joka käy kaikki CSV-tiedostot läpi
        for file in os.listdir(csv_folder):
            if file.endswith('.csv'): # Jos tiedosto on csv-tiedosto (varmistetaan, että prosessoidaan vain csv-tiedostoja)
                # Luetaan CSV tiedosto Pandasin Dataframeen
                df = pd.read_csv(os.path.join(csv_folder, file))
                print(f"{file} is being processed, its shape is {df.shape}")
                # Insertatataan, eli lisätään dataframen rivit tietokantatauluun
                conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
                files_processed += 1  # Montako tiedostoa prosessoitu
                
                # Printataan kuinka monta tiedostoa on jo prosessoitu
                print(f"{files_processed} / {csv_count} tiedostoa prosessoitu {time.time() - start_time:.2f} sekunnissa")

        print(f"Tiedostojen lisämiseen meni: {time.time() - start_time:.2f} sekunttia")
    else: # Ajetaan osa kannasta
        df = pd.read_csv(os.path.join(csv_folder, lite_file))
        print(f"{lite_file} is being processed, its shape is {df.shape}")
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        print(f"Lite tiedosto prosessoitu {time.time() - start_time:.2f} sekunnissa")
    
    conn.close() # Suljetaan tietokantayhteys

def insert_dataframe_into_table(df, table_name, database, insert=False):
    """
    df(pd.DataFrame): Pandasin dataframe, joka halutaan tallentaa
    table_name(str): tietokantataulun nimi, johon tallennetaan
    database(str): Pathi tietokanta tiedostoon
    insert(boolean): Lisätäänkö dataframe taulun jatkeeksi vai kirjoitetaanko päälle
    """
    conn = duckdb.connect(database=database, read_only=False) # Luodaan tietokanta yhteys
    if insert:
        print(f"Tallennetaan dataframe tietokantaan, jonka muoto on: {df.shape}")
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        print(f"Tallennus tauluun {table_name} onnistui")
    else:
        print(f"Tallennetaan dataframe tietokantaan, jonka muoto on: {df.shape}")
        df.to_sql(table_name, conn, index=False, if_exists='replace')
        print(f"Tallennus tauluun {table_name} onnistui")

def drop_table(table_name, db_file):
    # Connect to DuckDB
    conn = duckdb.connect(database=db_file, read_only=False)
    # Execute the SQL statement to drop the table
    conn.execute(f'DROP TABLE IF EXISTS {table_name}')
    conn.close()