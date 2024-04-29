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
file = "/code/data/duckdb.database"
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

# Hae päivämäärät valitussa kuukaudessa
def get_days_in_month(data, month):
    return sorted(data[data["Kuukausi"] == month]["Päivä"].unique())

# Hae sää valittuna päivänä
def get_weather_for_day(data, month, day):
    selected_day_data = data[(data["Kuukausi"] == month) & (data["Päivä"] == day)]
    return selected_day_data[(selected_day_data["Aika [Paikallinen aika]"] >= "09:00") & (selected_day_data["Aika [Paikallinen aika]"] <= "21:00")]

# Sovelluksen pääosa
def main():
    st.title(":mostly_sunny: Säätieto historiaa :mostly_sunny:")

    st.markdown(""" Säätietohistoriasta näemme, millainen sää on ollut silloin, kun kauppa on ollut auki kello 9-21 välillä.
""")
    
    # Lataa data
    file_path = "yhdistetty_sää.csv"  # Korvaa tiedostonimi omalla CSV-tiedostonimelläsi
    data = load_data(file_path)
    
    # Hae kuukaudet dataframesta
    months = get_months(data)
    
    # Dropdown-valikko kuukausien valitsemiseksi
    selected_month = st.selectbox("Valitse kuukausi", months)
    
    # Hae päivämäärät valitussa kuukaudessa
    days = get_days_in_month(data, selected_month)
    
    # Dropdown-valikko päivämäärien valitsemiseksi valitussa kuukaudessa
    selected_day = st.selectbox("Valitse päivä", days)
    
    # Näytä valitun päivän sää klo 9-21 välillä
    selected_day_data = get_weather_for_day(data, selected_month, selected_day)
    st.subheader(f"{selected_day}. {selected_month}")
    
    for index, row in selected_day_data.iterrows():
        st.write(f"**{row['Aika [Paikallinen aika]']}**")
        st.write(f"Lämpötila: {row['Ilman lämpötila keskiarvo [°C]']} °C :thermometer:")
        st.write(f"Suhteellinen kosteus: {row['Suhteellinen kosteus keskiarvo [%]']} % :droplet:")
        st.write(f"Lumensyvyys: {row['Lumensyvyys keskiarvo [cm]']} cm :snowflake:")
        st.write(f"Keskituulen nopeus: {row['Keskituulen nopeus keskiarvo [m/s]']} m/s :wind_blowing_face:")
        st.write(f"Sademäärä: {row['Sademäärä keskiarvo [mm]']} mm :rain_cloud:")
        st.write("---")

    
if __name__ == "__main__":
    main()