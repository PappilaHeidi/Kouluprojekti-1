import streamlit as st
import matplotlib.pyplot as plt
import os

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
selected_date = st.selectbox('Valitse aikaväli:', list(päivät.keys()))

# Näytä valittu kuva
image_path = päivät[selected_date]
image = plt.imread(image_path)

st.image(image, caption=f'Viikonpäivä: {selected_date}', use_column_width=True)
