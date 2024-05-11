import streamlit as st

st.set_page_config(
    page_title = "Muita tilastoja", 
    page_icon="📈",
    layout = "wide"
)


import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb

# Lataa kaupan pohjapiirros
def draw_store_layout(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    kassa_alue = [(80, 30), (180, 245)]
    kassa1 = [(80, 31), (180, 55)]

    kassa2 = [(80, 56), (180, 82)]

    kassa3 = [(80, 83), (180, 107)]

    kassa4 = [(80, 108), (180, 131)]

    kassa5 = [(80, 132), (180, 156)]

    kassa6 = [(80, 157), (180, 181)]

    kassa7 = [(80, 182), (180, 213)]

    kassa8 = [(80, 214), (180, 244)]

    # Määritä muut kassojen alueet tässä tarvittaessa
    draw.rectangle(kassa_alue, outline='red', width=2)
    draw.rectangle(kassa1, outline='green', width=2)
    draw.rectangle(kassa2, outline='blue', width=2)
    draw.rectangle(kassa3, outline='yellow', width=2)
    draw.rectangle(kassa4, outline='purple', width=2)
    draw.rectangle(kassa5, outline='brown', width=2)
    draw.rectangle(kassa6, outline='cyan', width=2)
    draw.rectangle(kassa7, outline='orange', width=2)
    draw.rectangle(kassa8, outline='pink', width=2)

    # Piirrä muut kassojen alueet tässä tarvittaessa
    return image

# Lataa tietokanta
def connect_to_database(database_path):
    return duckdb.connect(database=database_path)

# Hae data tietokannasta
def fetch_data_from_database(connection, kassojen_aluetta):
    query = """
        SELECT DISTINCT timestamp, x, y, node_id
        FROM Silver_SensorData
        WHERE x BETWEEN ? AND ? AND y BETWEEN ? AND ?
        AND EXTRACT(HOUR FROM timestamp) >= 9 AND EXTRACT(HOUR FROM timestamp) < 21
        AND CAST(timestamp AS TIME) >= '09:00:00' AND CAST(timestamp AS TIME) < '21:00:00'
        """
    params = (kassojen_aluetta[0][0], kassojen_aluetta[1][0], kassojen_aluetta[0][1], kassojen_aluetta[1][1])
    return connection.execute(query, params).fetchdf()

# Luo Streamlit-sovellus
def main():
    # Lataa kuva ja näytä se
    st.title('Kassojen analytiikka')
    image_path = 'kauppa.jpg'
    image = draw_store_layout(image_path)
    st.image(image, caption='Kaupan pohjapiirros kassojen alueella värikoodattuna', use_column_width=True)
    # Yhdistä tietokantaan
    connection = duckdb.connect(database='/code/data/duckdb.database')

    # Määritä kassojen alueet
    kassojen_aluetta = [(80, 30), (180, 245)]

    # Määritä kaikki mahdolliset node_id:t
    kaikki_node_id = ("3200", "3224", "3240", "42787", "45300", "51719", "51720", "51735", "51751", "51850", "51866", "51889", "51968", "51976", "51992", "52003", "52008", "52023", "52099", "52535", "53000", "53011", "53027", "53130", "53768", "53795", "53888", "53924", "53936", "54016", "64458")

    # Suorita SQL-kysely tietokannassa ja suodata tiedot suoraan kyselyssä
    query = """
        SELECT timestamp, x, y, node_id
        FROM Silver_SensorData
        WHERE x BETWEEN ? AND ? AND y BETWEEN ? AND ?
          AND EXTRACT(HOUR FROM timestamp) >= 9 AND EXTRACT(HOUR FROM timestamp) < 21
          AND CAST(timestamp AS TIME) >= '09:00:00' AND CAST(timestamp AS TIME) < '21:00:00'
          AND node_id IN {}
    """.format(kaikki_node_id)

    # Aseta parametrit kyselyyn
    params = (kassojen_aluetta[0][0], kassojen_aluetta[1][0], kassojen_aluetta[0][1], kassojen_aluetta[1][1])

    # Suorita kysely ja lue tulos DataFrameen
    df_filtered = connection.execute(query, params).fetchdf()

    # Näytä DataFrame, asiakkaiden määrä ja käytössä olevien kassojen määrä vierekkäin
    col1, col2 = st.columns(2)

    # Jaa aikaikkunat ja laske keskimääräinen asiakkaiden määrä kassojen alueella kullekin aikaikkunalle
    aikaikkunoiden_koko = '1H'  # Voit muuttaa aikaikkunoiden kokoa tarpeen mukaan
    df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])
    df_filtered.set_index('timestamp', inplace=True)
    asiakaslkm_aikaikkunoissa = df_filtered.groupby(pd.Grouper(freq=aikaikkunoiden_koko)).size()

    # Ryhmittele DataFrame timestampin ja node_id:n perusteella ja laske jokaiselle aukioloajan tunti- ja päiväkohtaisesti käytössä olevien kassojen määrä
    kassojen_maara_aikapisteittain = df_filtered.groupby([pd.Grouper(freq='H'), df_filtered.index.dayofweek, df_filtered.index.hour])['node_id'].nunique()

    # Tulosta asiakkaiden määrä kassojen alueella kullekin aikaikkunalle
    col1.subheader('Asiakkaiden määrä kassojen alueella kullekin aikaikkunalle:')
    col1.write(asiakaslkm_aikaikkunoissa)

    # Tulosta käytössä olevien kassojen määrä eri aukioloaikoina eri päivinä
    col2.subheader('Käytössä olevien kassojen määrä eri aukioloaikoina eri päivinä:')
    col2.write(kassojen_maara_aikapisteittain)

    # Näytä histogrammi kassojen määrästä
    st.subheader('Histogrammi - Kassojen määrä')
    plt.figure(figsize=(10, 6))
    plt.hist(df_filtered['node_id'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogrammi - Kassojen määrä')
    plt.xlabel('Kassojen määrä')
    plt.ylabel('Taajuus')
    plt.grid(True)
    st.pyplot()

    # Näytä scatter-plot kassojen sijainnista
    st.subheader('Scatter-plot - Kassojen sijainti')
    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtered['x'], df_filtered['y'], alpha=0.5)
    plt.title('Scatter-plot - Kassojen sijainti')
    plt.xlabel('X-koordinaatti')
    plt.ylabel('Y-koordinaatti')
    plt.grid(True)
    st.pyplot()

    # Näytä pylväsdiagrammi kassojen määrästä eri aukioloaikoina eri päivinä
    st.subheader('Pylväsdiagrammit - Kassojen määrä eri aukioloaikojen tunteina eri päivinä')
    df_kassojen_maara = kassojen_maara_aikapisteittain.unstack()
    plt.figure(figsize=(12, 6))
    df_kassojen_maara.plot(kind='bar', stacked=True)
    plt.title('Pylväsdiagrammit - Kassojen määrä eri aukioloaikojen tunteina eri päivinä')
    plt.xlabel('Aukioloaika')
    plt.ylabel('Kassojen määrä')
    plt.grid(True)
    st.pyplot()

    # Sulje yhteys tietokantaan
    connection.close()

if __name__ == "__main__":
    main()