import streamlit as st
import pandas as pd
import gigafunctions as giga
import numpy as np

# Asetetaan sivu
st.set_page_config(
    page_title = "Säätietoa", 
    page_icon=":mostly_sunny:",
    layout = "wide"
)

# Vähän tyyliä streamlittiin
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
    }
    .big {
        font-size: 32px;
        margin-left: -300px; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Avataan data streamlittiin
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Haetaan kuukaudet ja muutetaan ne nämän nimisiksi
def get_months(data):
    months_names = ["Tammikuu-2020", "Helmikuu", "Maaliskuu-2019", "Huhtikuu-2019", "Toukokuu-2019", "Kesäkuu-2019", "Heinäkuu-2019", "Elokuu-2019", "Syyskuu-2019", "Lokakuu-2019", "Marraskuu-2019", "Joulukuu-2019"]
    
    # Järjestetään kuukaudet niin, että tammikuu-2020 viimeisenä
    data["Kuukausi"] = data["Kuukausi"].map(lambda x: months_names[x-1])
    return sorted(data["Kuukausi"].unique(), key=lambda x: months_names.index(x) if x != "Tammikuu-2020" else float("inf"))

# Sovelluksen pääosa
def main():
    st.title(":mostly_sunny: Säätieto historiaa :mostly_sunny:")
    
    st.markdown(""" **Valitsemalla "Kaikki päivät" näet valitun kuukauden sään keskiarvot, sekä kuukauden asiakasmäärän. Valitsemalla "Yksittäinen päivä" näet tietyn päivän säätiedot, sekä sen päivän asiakasmäärän.**
    """)

    st.markdown("""*Sarakkeen "Lumensyvyys" tiedot jätetään pois niiltä kuukaisilta, joissa se on 0 tai alle dataframessa*""")

    # Ladataan säätieto data
    file_path = "yhdistetty_sää.csv"
    data = load_data(file_path)

    # Muunnetaan sarakkeet numeerisiksi niin voidaan saada sään keskiarvot
    numeric_columns = ['Ilman lämpötila keskiarvo [°C]', 'Suhteellinen kosteus keskiarvo [%]', 'Sademäärä keskiarvo [mm]', 'Lumensyvyys keskiarvo [cm]', 'Keskituulen nopeus keskiarvo [m/s]']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Hae kuukaudet dataframesta
    months = get_months(data)

    # Dropdown-valikko kuukausien valitsemiseksi
    selected_month = st.selectbox("Valitse kuukausi:", months)

    # Vaihtoehto kaikkien päivien tai oman päivän valitsemiseksi
    selection_option = st.sidebar.radio("Valitse: ", ("Kaikki päivät", "Yksittäinen päivä"))

    # Jos valitaan "Kaikki päivät" niin saadaan näkyviin vain kuukauden keskiarvot
    if selection_option == "Kaikki päivät":
        st.write(" ")
        st.markdown('<p class="center big"><b>📊 {} asiakasmäärä & sään keskiarvot 📊</b></p>'.format(selected_month), unsafe_allow_html=True)
        st.write(" ")

        # Lisätään streamlittiin 2 saraketta
        col = st.columns(2)

        with col[1]:
            # Otetaan kuukaudet ja lasketaan kuukausien keskiarvot
            month_data = data[data["Kuukausi"] == selected_month]
            month_data_numeric = month_data.select_dtypes(include=[float])
            month_mean = month_data_numeric.mean()

            # Lasketaan aiempien kuukausien keskiarvot
            previous_month = months[months.index(selected_month) - 1]
            previous_month_data = data[data["Kuukausi"] == previous_month]
            previous_month_data_numeric = previous_month_data.select_dtypes(include=[float])
            previous_month_mean = previous_month_data_numeric.mean()

            # Lasketaan erotus nykyisen ja aiemma kuukauden välillä
            temperature_change = round(month_mean['Ilman lämpötila keskiarvo [°C]'] - previous_month_mean['Ilman lämpötila keskiarvo [°C]'], 1)
            humidity_change = round(month_mean['Suhteellinen kosteus keskiarvo [%]'] - previous_month_mean['Suhteellinen kosteus keskiarvo [%]'], 1)
            snow_depth = round(month_mean['Lumensyvyys keskiarvo [cm]'] - previous_month_mean['Lumensyvyys keskiarvo [cm]'], 1)
            rain_change = round(month_mean['Sademäärä keskiarvo [mm]'] - previous_month_mean['Sademäärä keskiarvo [mm]'], 2)
            wind_change = round(month_mean['Keskituulen nopeus keskiarvo [m/s]'] - previous_month_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)

            # Näytetään nykyisen kuukauden tiedot, sekä yllä laskettu erotus + pyöristetään sopivaan lukuun
            st.metric("Lämpötilan keskiarvo", f"{np.around(month_mean['Ilman lämpötila keskiarvo [°C]'], 1)} °C", f"{temperature_change} °C")
            st.metric("Suhteellisen kosteuden keskiarvo", f"{np.around(month_mean['Suhteellinen kosteus keskiarvo [%]'], 1)} %", f"{humidity_change} %")
            st.metric("Sademäärän keskiarvo", f"{np.around(month_mean['Sademäärä keskiarvo [mm]'], 2)} mm", f"{rain_change} mm")   
            st.metric("Keskituulen nopeuden keskiarvo", f"{np.around(month_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)} m/s", f"{wind_change} m/s") 
            # Jos kuukausi ei ole joku näistä niin lumensyvyys rivi jää pois
            if selected_month in ["Tammikuu-2020", "Maaliskuu-2019", "Joulukuu-2019", "Marraskuu-2019"]:
                st.metric("Lumensyvyyden keskiarvo", f"{np.around(month_mean['Lumensyvyys keskiarvo [cm]'], 1)} cm", f"{snow_depth} cm")   
    
        with col[0]:
            # Lasketaan kuukauden asiakasmäärä ja näytetään se metricin avulla
            month_customer_count = giga.count_paths(month_data)
            # Lasketaan verrataan aiempaan kuukauteen
            previous_month_count = giga.count_paths(previous_month_data)
            month_dif = month_customer_count - previous_month_count
            st.metric("Kuukauden kokonaisasiakasmäärä:", month_customer_count, month_dif)
            st.write("")
            st.write("")

            # Kuukausien nimet ja lisätään asiakasmäärät oikeisiin kuukausiin
            months_names = ["Maaliskuu-2019", "Huhtikuu-2019", "Toukokuu-2019", "Kesäkuu-2019", "Heinäkuu-2019", "Elokuu-2019", "Syyskuu-2019", "Lokakuu-2019", "Marraskuu-2019", "Joulukuu-2019", "Tammikuu-2020"]
            month_customer_counts = [giga.count_paths(data[data["Kuukausi"] == month]) for month in months_names]

            # Luodaan oma dataframe asiakasmäärille ja kuukausille
            data = {'Kuukausi': months_names, 'Asiakasmäärä': month_customer_counts}
            df = pd.DataFrame(data)

            # Järjestetään ne oikein
            df["Kuukausi"] = pd.Categorical(df["Kuukausi"], categories=months_names, ordered=True)
            df = df.sort_values(by="Kuukausi")

            # Luodaan pylväsdiagrammi
            st.bar_chart(df.set_index('Kuukausi'), use_container_width=True)

    else:
        # Näytä yksittäisen päivän tiedot
        st.markdown(""" **Tällä sivulla on tarkoitus näyttää valitun päivän asiakasmäärä, sekä saman päivän sää. Tätä muokataan vielä...**
        """)
        st.subheader("Yksittäisen päivän sää")
        # Hae päivämäärät valitussa kuukaudessa
        days = sorted(data[data["Kuukausi"] == selected_month]["Päivä"].unique())
        selected_day = st.sidebar.selectbox("Valitse päivä:", days)  # Näytä valittu päivä
        selected_day_data = data[(data["Kuukausi"] == selected_month) & (data["Päivä"] == selected_day)]
        
        # Näytä valitun päivän sää klo 9-21 välillä
        with st.expander("Täältä löytyy tarkempaa säätä"):
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