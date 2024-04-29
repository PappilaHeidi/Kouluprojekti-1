import streamlit as st
import pandas as pd
import duckdb
import os

st.set_page_config(
    page_title = "Säätietoa", 
    page_icon=":mostly_sunny:",
    layout = "wide"
)

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def read_node(tbl:str, node_name:str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetchdf()
    con.close()
    return df

# Lue asiakastiedot tietokannasta
file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "duckdb.database"))
tbl = "Silver_SensorData"
node = "3200"
customer_data = read_node(tbl, node, file)

# Hae kuukaudet
def get_months(data):
    # Kuukausien nimet
    months_names = ["Tammikuu-2020", "Helmikuu", "Maaliskuu-2019", "Huhtikuu-2019", "Toukokuu-2019", "Kesäkuu-2019", "Heinäkuu-2019", "Elokuu-2019", "Syyskuu-2019", "Lokakuu-2019", "Marraskuu-2019", "Joulukuu-2019"]
    
    # Muunna numerot kuukausien nimiksi ja järjestä ne
    data["Kuukausi"] = data["Kuukausi"].map(lambda x: months_names[x-1])
    return sorted(data["Kuukausi"].unique(), key=lambda x: months_names.index(x) if x != "Tammikuu-2020" else float("inf"))

# Sovelluksen pääosa
def main():
    st.title(":mostly_sunny: Säätieto historiaa :mostly_sunny:")
    
    st.markdown(""" **Valitsemalla "Kaikki päivät" näet valitun kuukauden sään keskiarvot. Valitsemalla "Yksittäinen päivä" näet tietyn päivän säätiedot.**
    """)

    # Lataa data
    file_path = "yhdistetty_sää.csv"  # Korvaa tiedostonimi omalla CSV-tiedostonimelläsi
    data = load_data(file_path)

    # Muunna sarakkeet numeerisiksi
    numeric_columns = ['Ilman lämpötila keskiarvo [°C]', 'Suhteellinen kosteus keskiarvo [%]', 'Sademäärä keskiarvo [mm]', 'Lumensyvyys keskiarvo [cm]', 'Keskituulen nopeus keskiarvo [m/s]']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Hae kuukaudet dataframesta
    months = get_months(data)

    # Dropdown-valikko kuukausien valitsemiseksi
    selected_month = st.selectbox("Valitse kuukausi:", months)

    # Vaihtoehto kaikkien päivien tai oman päivän valitsemiseksi
    selection_option = st.sidebar.radio("Valitse: ", ("Kaikki päivät", "Yksittäinen päivä"))

    if selection_option == "Kaikki päivät":
        st.markdown(""" **Tällä sivulla on tarkoitus näyttää valitun kuukauden asiakasmäärä, sekä saman kuukauden keskiarvot säästä. Tätä muokataan vielä...**
        """)
        st.markdown("""*Sarakkeen "Lumensyvyys" tiedot jätetään pois niiltä kuukaisilta, joissa se on 0 tai alle dataframessa*""")
        # Näytä vain kuukauden kaikkien päivien keskiarvot
        st.subheader(f"📊 {selected_month} sään keskiarvot: 📊")
        st.write(" ")
        month_data = data[data["Kuukausi"] == selected_month]
        month_data_numeric = month_data.select_dtypes(include=[float])
        month_mean = month_data_numeric.mean().round(2)

        st.write(f"Lämpötilan keskiarvo: {month_mean['Ilman lämpötila keskiarvo [°C]']} °C 🌡️")
        st.write(f"Suhteellisen kosteuden keskiarvo: {month_mean['Suhteellinen kosteus keskiarvo [%]']} % 💧")    
        # Näytä "Lumensyvyys keskiarvo [cm]" -sarake vain tammikuulle, maaliskuulle, joulukuulle ja marraskuulle
        if selected_month in ["Tammikuu-2019", "Maaliskuu-2019", "Joulukuu-2019", "Marraskuu-2019"]:
            st.write(f"Lumensyvyyden keskiarvo: {month_mean['Lumensyvyys keskiarvo [cm]']} cm ❄️")   
        st.write(f"Keskituulen nopeuden keskiarvo: {month_mean['Keskituulen nopeus keskiarvo [m/s]']} m/s 🌬️")
        st.write(f"**Sademäärän keskiarvo:** {month_mean['Sademäärä keskiarvo [mm]']} mm 🌧️")

    else:
        # Näytä yksittäisen päivän tiedot
        st.markdown(""" **Tällä sivulla on tarkoitus näyttää valitun päivän asiakasmäärä, sekä saman päivän sää. Tätä muokataan vielä...**
        """)
        st.markdown("""*Sarakkeen "Lumensyvyys" tiedot jätetään pois niiltä tunneilta, joissa se on 0 tai alle dataframessa.*""")
        st.subheader("Yksittäisen päivän sää")
        # Hae päivämäärät valitussa kuukaudessa
        days = sorted(data[data["Kuukausi"] == selected_month]["Päivä"].unique())
        selected_day = st.sidebar.selectbox("Valitse päivä:", days)  # Näytä valittu päivä
        selected_day_data = data[(data["Kuukausi"] == selected_month) & (data["Päivä"] == selected_day)]
        
        # Näytä valitun päivän sää klo 9-21 välillä
        with st.expander("Sää kaupan aukioloaikoina"):
            selected_day_data_time = selected_day_data[
                (selected_day_data["Aika [Paikallinen aika]"] >= "09:00") & 
                (selected_day_data["Aika [Paikallinen aika]"] <= "21:00")
            ]
            for index, row in selected_day_data_time.iterrows():
                st.write(f"**{row['Aika [Paikallinen aika]']}**")
                st.write(f"Lämpötila: {row['Ilman lämpötila keskiarvo [°C]']} °C :thermometer:")
                st.write(f"Suhteellinen kosteus: {row['Suhteellinen kosteus keskiarvo [%]']} % :droplet:")
                lumensyvyys = float(row['Lumensyvyys keskiarvo [cm]'])
                if lumensyvyys > 0:
                    st.write(f"Lumensyvyys: {lumensyvyys} cm :snowflake:")
                st.write(f"Keskituulen nopeus: {row['Keskituulen nopeus keskiarvo [m/s]']} m/s :wind_blowing_face:")
                st.write(f"Sademäärä: {row['Sademäärä keskiarvo [mm]']} mm :rain_cloud:")

if __name__ == "__main__":
    main()