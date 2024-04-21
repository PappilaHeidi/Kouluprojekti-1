import streamlit as st
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import duckdb

st.set_page_config(
    page_title = "Heatmap",
    page_icon="😅",
    layout = "wide"
)

st.title('Heidin GIGAHeatmap')

st.markdown("""
            Kaupanmapin kuumat kohteet tulostettuna lämpimillä(Punainen 😡) ja kylmillä väreillä (Valkoinen 💀)""")

st.markdown("""(Toimii nyt tällä hetkellä Heidin luomien kuvien kautta, ei siis sisällä kompleksia koodia) """)

# Esimerkkipohja kuvatiedostojen poluille
kellonajat = {
    '9-11': 'heatmap-animaatio/heatmap-kuvat/heatmap_9_to_11.png',
    '11-13': 'heatmap-animaatio/heatmap-kuvat/heatmap_11_to_13.png',
    '13-15': 'heatmap-animaatio/heatmap-kuvat/heatmap_13_to_15.png',
    '15-17': 'heatmap-animaatio/heatmap-kuvat/heatmap_15_to_17.png',
    '17-19': 'heatmap-animaatio/heatmap-kuvat/heatmap_17_to_19.png',
    '19-21': 'heatmap-animaatio/heatmap-kuvat/heatmap_19_to_21.png',
    # Lisää kuvatiedostojen polut tähän
}

# Streamlit sovelluksen otsikko
st.title('🔥 Kuumimmat alueet haluttujen aikavälien mukaan 🔥')

# Valitse päivä dropdownista
selected_date = st.selectbox('Valitse aikaväli:', list(kellonajat.keys()))

# Näytä valittu kuva
image_path = kellonajat[selected_date]
image = plt.imread(image_path)

st.image(image, caption=f'Kuva ajalta {selected_date}', use_column_width=True)


# Esimerkkipohja kuvatiedostojen poluille
päivät = {
    'Maanantai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_1Monday.png',
    'Tiistai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_2Tuesday.png',
    'Keskiviikko': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_3Wednesday.png',
    'Torstai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_4Thursday.png',
    'Perjantai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_5Friday.png',
    'Lauantai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_6Saturday.png',
    'Sunnuntai': 'heatmap-animaatio/heatmap-viikonpäivä/heatmap_7Sunday.png',
    # Lisää kuvatiedostojen polut tähän
}

# Streamlit sovelluksen otsikko
st.title('Päivän kuumimmat 🥵')

# Valitse päivä dropdownista
selected_date = st.selectbox('Valitse viikonpäivä:', list(päivät.keys()))

# Näytä valittu kuva
image_path = päivät[selected_date]
image = plt.imread(image_path)

st.image(image, caption=f'Viikonpäivä: {selected_date}', use_column_width=True)

# Tähän joku giga magee koodi rimpsu mistä saadaan ite valita kellon ajat

# Avataan tietokanta ja valitaan oikea datasetti
def read_node(tbl: str, node_name: str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetch_df()
    con.close()
    return df

# Määritä projektin juuripolku
IMG_PATH = "/app/code/kauppa.jpg"

# Lataa data
@st.cache_data()
def load_data(file: str, tbl: str, node: str):
    df = read_node(tbl, node, file)
    return df

file = "/data/duckdb.database"
tbl = "Silver_SensorData"
node = st.sidebar.selectbox("Valitse node:", ["3200", "3224", "3240", "42787", "45300", "51719", "51720", "51735", "51751", "51850", "51866", "51889", "51968", "51976", "51992", "52003", "52008", "52023", "52099", "52535", "53000", "53011", "53027", "53130", "53768", "53795", "53888", "53924", "53936", "54016", "64458"])

df = load_data(file, tbl, node)

# Pienennetään dataa siten, että otetaan kuvan ulkopuolella olevat datapisteet pois
df_lim = df[(df['x'] >= 305) & (df['x'] <= 1250) & (df['y'] <= 560)]

# Luo heatmap
st.title('🔥 Kuumimmat alueet halutun aikavälin mukaan 🔥')

# Valitse aikaväli
start_hour = st.slider("Valitse aloitusaika:", 9, 21, 9)
end_hour = st.slider("Valitse lopetusaika:", 9, 21, 11)

# Rajaa data valitulle aikavälille
selected_data = df_lim[(df_lim['timestamp'].dt.hour >= start_hour) & (df_lim['timestamp'].dt.hour < end_hour)]

# Lataa kuva
@st.cache_resource
def load_image(path):
    return plt.imread(path)

img = load_image(IMG_PATH)
img_height, img_width, _ = img.shape

# Luo heatmap
fig, ax = plt.subplots(figsize=(13, 13))
sns.kdeplot(data=selected_data, x='x', y='y', cmap="Reds", shade=True, bw=.15, alpha=1, ax=ax)
plt.imshow(img, zorder=0, extent=[0, img_width, 0, img_height], alpha=1)
plt.title(f"Aikaväli {start_hour}:00-{end_hour}:00")
st.pyplot(fig)
