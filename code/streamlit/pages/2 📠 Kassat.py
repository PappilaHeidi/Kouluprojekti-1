import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb
import datetime

# Lataa kaupan pohjapiirros
def draw_store_layout(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    kassa_alue = [(80, 30), (158, 245)]  
    kassa1 = [(80, 31), (158, 55)]
    kassa2 = [(80, 56), (158, 82)]
    kassa3 = [(80, 83), (158, 107)]
    kassa4 = [(80, 108), (158, 131)]
    kassa5 = [(80, 132), (158, 156)]
    kassa6 = [(80, 157), (158, 181)]
    kassa7 = [(80, 182), (158, 213)]
    kassa8 = [(80, 214), (158, 244)]
    
    draw.rectangle(kassa_alue, outline='red', width=2)
    draw.rectangle(kassa1, outline='green', width=2)
    draw.rectangle(kassa2, outline='blue', width=2)
    draw.rectangle(kassa3, outline='yellow', width=2)
    draw.rectangle(kassa4, outline='purple', width=2)
    draw.rectangle(kassa5, outline='brown', width=2)
    draw.rectangle(kassa6, outline='cyan', width=2)
    draw.rectangle(kassa7, outline='orange', width=2)
    draw.rectangle(kassa8, outline='pink', width=2)
    return image

# Lataa tietokanta
def connect_to_database(database_path):
    return duckdb.connect(database=database_path)

# Hae data tietokannasta
def fetch_data_from_database(connection, kassojen_aluetta):
    query = """
        SELECT timestamp, x, y, node_id,
        EXTRACT(HOUR FROM timestamp) AS hour  -- Lisätään tunnin tieto
        FROM Silver_SensorData
        WHERE x BETWEEN ? AND ? AND y BETWEEN ? AND ?
          AND EXTRACT(HOUR FROM timestamp) >= 9 AND EXTRACT(HOUR FROM timestamp) < 21
          AND CAST(timestamp AS TIME) >= '09:00:00' AND CAST(timestamp AS TIME) < '21:00:00'
    """
    params = (kassojen_aluetta[0][0], kassojen_aluetta[1][0], kassojen_aluetta[0][1], kassojen_aluetta[1][1])
    return connection.execute(query, params).fetchdf()

# Luo Streamlit-sovellus
def main():
    st.set_page_config(page_title="📠 Kassojen analytiikka 📠", page_icon="📠", layout="wide")
    st.title('Kassojen analytiikka')
    st.markdown("""---""")

    st.markdown("""
    ## Tervetuloa Kassojen analytiikka -sovellukseen! 

    Tämä sovellus tarjoaa interaktiivisen tavan tarkastella kaupan kassojen alueen liikennettä ja asiakasmääriä. 
        Sovelluksen avulla voit tehdä seuraavia asioita:
        - Tutkia kaupan pohjapiirrosta ja kassojen sijainteja
        - Tarkastella kassojen käyttöä eri tunteina ja päivinä
        - Seurata asiakasmääriä kassojen alueella eri aikaväleillä
        
        Valitse haluamasi ajanjakso vasemmalta sidebarista ja tutustu kaupan kassatarpeisiin!
    """)

    st.markdown("""---""")

    # Pohjapiirros ja scatter-plot
    image_path = 'kauppa.jpg'
    image = draw_store_layout(image_path)

 
    st.subheader('Kaupan pohjapiirros kassojen alueella')
    st.image(image, width=500, use_column_width=True)

    # Yhdistä tietokantaan
    connection = connect_to_database('/code/data/duckdb.database')

    # Haetaan data tietokannasta
    df_filtered = fetch_data_from_database(connection, [(80, 30), (158, 245)])

    # Sulje tietokantayhteys
    connection.close()

    # Jaa aikaikkunat ja laske keskimääräinen asiakkaiden määrä kassojen alueella kullekin aikaikkunalle
    aikaikkunoiden_koko = '1H'  # Voit muuttaa aikaikkunoiden kokoa tarpeen mukaan
    df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])
    df_filtered.set_index('timestamp', inplace=True)
    asiakaslkm_aikaikkunoissa = df_filtered.groupby(pd.Grouper(freq=aikaikkunoiden_koko)).size()

    # Lisää valintakentät käyttäjälle
    st.sidebar.header('Valitse ajanjakso')
    df_filtered['date'] = df_filtered.index.date
    df_filtered['month'] = df_filtered.index.month
    df_filtered['year'] = df_filtered.index.year
    df_filtered['week'] = df_filtered.index.isocalendar().week

    # Määritä kuukaudet suomen kielellä vuosien 2019 ja 2020 mukaan
    months_dict = {
        1: 'Tammikuu', 2: 'Helmikuu', 3: 'Maaliskuu', 4: 'Huhtikuu', 5: 'Toukokuu', 6: 'Kesäkuu',
        7: 'Heinäkuu', 8: 'Elokuu', 9: 'Syyskuu', 10: 'Lokakuu', 11: 'Marraskuu', 12: 'Joulukuu'
    }
    df_filtered['Kuukausi'] = df_filtered.apply(lambda x: f"{months_dict[x['month']]}-{x['year']}", axis=1)
    
    # Määritä kuukaudet ja vuodet oikeassa järjestyksessä
    months_order = [
        "Maaliskuu-2019", "Huhtikuu-2019", "Toukokuu-2019", "Kesäkuu-2019",
        "Heinäkuu-2019", "Elokuu-2019", "Syyskuu-2019", "Lokakuu-2019", "Marraskuu-2019", "Joulukuu-2019", "Tammikuu-2020"
    ]
    unique_months = sorted(df_filtered['Kuukausi'].unique(), key=lambda x: months_order.index(x))

    # Aseta oletuskuukausi ja -viikko
    default_month = "Maaliskuu-2019"
    default_week = 13

    selected_month_name = st.sidebar.selectbox('Kuukausi', unique_months)

    # Näytä valintakentät vain, kun kuukausi on valittu
    if selected_month_name:
        unique_weeks = df_filtered[df_filtered['Kuukausi'] == selected_month_name]['week'].unique()
        selected_week = st.sidebar.selectbox('Viikko', sorted(unique_weeks))

        # Suodata data valitun kuukauden ja viikon perusteella
        df_filtered = df_filtered[(df_filtered['Kuukausi'] == selected_month_name) & (df_filtered['week'] == selected_week)]

    # Ryhmittele DataFrame timestampin, päivän ja tunnin perusteella ja laske jokaiselle aukioloajan tunti- ja päiväkohtaisesti käytössä olevien kassojen määrä
    kassojen_maara_aikapisteittain = df_filtered.groupby([pd.Grouper(freq='H'), df_filtered.index.dayofweek])['node_id'].nunique()

    # Muuta indeksin nimet
    kassojen_maara_aikapisteittain.index.set_names(['Hour', 'dayofweek'], inplace=True)

    # Nollaa indeksi
    kassojen_maara_df = kassojen_maara_aikapisteittain.reset_index().rename(columns={'node_id': 'Kassojen määrä'})

    # Muuta dayofweek-numeroiden nimet 1-7
    kassojen_maara_df['dayofweek'] = kassojen_maara_df['dayofweek'] + 1

    # Näytä scatter-plot kärryt kassalla

    st.subheader('Scatter-plot - Kärryn sijainti kassa-alueella')
    st.markdown("Tämä scatter-plot näyttää kärryjen sijainnin kassa-alueella, mikä auttaa havainnollistamaan asiakkaiden liikkumista kassalla.")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_filtered['x'], df_filtered['y'], alpha=0.5)
    ax.set_title('Scatter-plot - Kärryn sijainti kassa-alueella')
    ax.set_xlabel('X-koordinaatti')
    ax.set_ylabel('Y-koordinaatti')
    ax.grid(True)
    st.pyplot(fig)

    col3, col4 = st.columns(2)

    # Pylväsdiagrammit
    with col3:
        st.subheader('Kassojen määrä eri tunteina')
        st.markdown("Tämä pylväsdiagrammi esittää kassojen määrän eri tunteina viikonpäivittäin.")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=kassojen_maara_df, x='Hour', y='Kassojen määrä', hue='dayofweek', ax=ax1)
        ax1.set_title('Pylväsdiagrammi - Kassojen määrä eri tunteina')
        ax1.set_xlabel('Tunti')
        ax1.set_ylabel('Kassojen määrä')
        ax1.legend(title='Viikonpäivä')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)  # Käännetään tuntien merkinnät
        ax1.grid(True)
        st.pyplot(fig1)

    with col4:
        st.subheader('Kassojen määrä eri päivinä')
        st.markdown("Tämä pylväsdiagrammi esittää kassojen määrän eri päivinä tuntikohtaisesti.")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=kassojen_maara_df, x='dayofweek', y='Kassojen määrä', hue='Hour', ax=ax2)
        ax2.set_title('Pylväsdiagrammi - Kassojen määrä eri päivinä')
        ax2.set_xlabel('Viikonpäivä')
        ax2.set_ylabel('Kassojen määrä')
        ax2.legend(title='Tunti')


        ax2.grid(True)
        st.pyplot(fig2)

    # Line plot
    st.subheader('Asiakkaiden määrä kassojen alueella kullekin aikaikkunalle')
    st.markdown("Tämä lineaarinen kuvaaja esittää asiakkaiden määrän kassojen alueella kullekin aikaikkunalle.")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    asiakaslkm_aikaikkunoissa.plot(kind='line', color='blue', ax=ax3)
    ax3.set_title('Asiakkaiden määrä kassojen alueella kullekin aikaikkunalle')
    ax3.set_xlabel('Aika')
    ax3.set_ylabel('Asiakkaiden määrä')
    ax3.grid(True)
    st.pyplot(fig3)

if __name__ == "__main__":
    main()
