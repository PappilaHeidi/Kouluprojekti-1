import streamlit as st
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import duckdb

st.set_page_config(
    page_title="Heatmap",
    page_icon="😅",
    layout="wide"
)

st.title('Heatmap')

st.markdown("""
            Kaupan kartan kuumat kohteet tulostettuna lämpimillä (Punainen 😡) ja kylmillä väreillä (Valkoinen 💀).
            Tämä visualisointi auttaa tunnistamaan alueet, joilla asiakkaat viettävät eniten aikaa kaupassa.
            """)

# Avataan tietokanta ja valitaan oikea datasetti
def read_node(tbl: str, node_name: str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetch_df()
    con.close()
    return df

# Määritä projektin juuripolku
IMG_PATH = "/code/kauppa.jpg"

# Lataa data
@st.cache_data()
def load_data(file: str, tbl: str, node: str):
    df = read_node(tbl, node, file)
    return df

file = "/code/data/duckdb.database"
tbl = "Silver_SensorData"
node = st.sidebar.selectbox("Valitse node:", ["3200", "3224", "3240", "42787", "45300", "51719", "51720", "51735", "51751", "51850", "51866", "51889", "51968", "51976", "51992", "52003", "52008", "52023", "52099", "52535", "53000", "53011", "53027", "53130", "53768", "53795", "53888", "53924", "53936", "54016", "64458"])

df = load_data(file, tbl, node)

# Pienennetään dataa siten, että otetaan kuvan ulkopuolla olevat datapisteet pois
df_lim = df[(df['x'] >= 305) & (df['x'] <= 1250) & (df['y'] <= 560)]

# Lataa kuva
@st.cache_resource
def load_image(path):
    return plt.imread(path)

img = load_image(IMG_PATH)
img_height, img_width, _ = img.shape

st.title('🔥 Kuumimmat alueet halutun aikavälin mukaan 🔥')

st.markdown("""
            Tässä osiossa voit valita aikavälin ja nähdä kaupan kuumimmat alueet kyseisenä aikana.
            Käytä liukusäätimiä valitaksesi haluamasi aloitus- ja lopetusajan.
            """)

# Valitse aikaväli
start_hour = st.slider("Valitse aloitusaika:", 9, 21, 9)
end_hour = st.slider("Valitse lopetusaika:", 9, 21, 11)

valid_time_range = True

if start_hour == end_hour:
    st.error("Valitse eri aloitus- ja lopetusaika.")
    valid_time_range = False
elif start_hour > end_hour:
    st.error("Lopetusajan on oltava suurempi kuin aloitusajan.")
    valid_time_range = False

if valid_time_range:
    # Rajaa data valitulle aikavälille
    selected_data = df_lim[(df_lim['timestamp'].dt.hour >= start_hour) & (df_lim['timestamp'].dt.hour < end_hour)]

    # Luo heatmap aikavälin perusteella
    fig, ax = plt.subplots(figsize=(13, 13))
    hmax = sns.kdeplot(data=selected_data, x='x', y='y', cmap="Reds", shade=True, bw=.15, alpha=0.6, ax=ax)
    ax.imshow(img, zorder=0, extent=[0, img_width, 0, img_height], alpha=1)
    plt.title(f"Aikaväli {start_hour}:00-{end_hour}:00")
    plt.colorbar(hmax.collections[0], fraction=0.02)
    st.pyplot(fig)

# Lisätään viikonpäivä-sarake
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['weekday'] = df['timestamp'].dt.day_name()

st.title('🥵 Viikonpäivän kuumimmat 🥵')

st.markdown("""
            Tässä osiossa voit valita viikonpäivän ja nähdä kaupan kuumimmat alueet kyseisenä päivänä.
            Valitse viikonpäivä alla olevasta valikosta.
            """)

if valid_time_range:
    # Valitse viikonpäivä
    fin_to_eng_weekdays = {
        'Maanantai': 'Monday',
        'Tiistai': 'Tuesday',
        'Keskiviikko': 'Wednesday',
        'Torstai': 'Thursday',
        'Perjantai': 'Friday',
        'Lauantai': 'Saturday',
        'Sunnuntai': 'Sunday'
    }

    # Valitse viikonpäivä
    selected_day = st.selectbox('Valitse viikonpäivä:', ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai', 'Sunnuntai'])
    selected_day_eng = fin_to_eng_weekdays[selected_day]

    # Rajaa data valitulle viikonpäivälle ja piirrä heatmap
    df_lim_weekday = df[(df['x'] >= 305) & (df['x'] <= 1250) & (df['y'] <= 560) & (df['weekday'] == selected_day_eng)]
    fig, ax = plt.subplots(figsize=(13, 13))
    hmax_weekday = sns.kdeplot(data=df_lim_weekday, x='x', y='y', cmap="Reds", shade=True, bw=.15, alpha=0.6)
    plt.imshow(img, zorder=0, extent=[0, img_width, 0, img_height], alpha=1)
    plt.title(selected_day)
    st.pyplot(fig)
else:
    st.warning("Valitse ensin aikaväli ennen viikonpäivän valitsemista.")
