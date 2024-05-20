import streamlit as st
import pandas as pd
import gigafunctions as giga
import numpy as np
import altair as alt
from multiprocessing import Pool


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

def available_nodes():
    nodes = giga.fetch_nodes() #fetch all nodes in db
    node_list = sorted([int(str(x[0])) for x in nodes])
    return node_list

# Sovelluksen pääosa
def main():
    st.title(":mostly_sunny: Säätieto historiaa :mostly_sunny:")
    
    st.markdown(""" **Valitsemalla "Kaikki päivät" näet valitun kuukauden sään keskiarvot, sekä kuukauden asiakasmäärän. Valitsemalla "Yksittäinen päivä" näet tietyn päivän säätiedot, sekä sen päivän asiakasmäärän.**
    """)
    st.markdown("""*Sarakkeen "Lumensyvyys" tiedot jätetään pois niiltä kuukausilta, joissa se on 0 tai alle dataframessa*""")
    # Ladataan säätieto data
    file_path = "yhdistetty_sää.csv"
    data = load_data(file_path)
    # Muunnetaan sarakkeet numeerisiksi niin voidaan saada sään keskiarvot
    numeric_columns = ['Ilman lämpötila keskiarvo [°C]', 'Suhteellinen kosteus keskiarvo [%]', 'Sademäärä keskiarvo [mm]', 'Lumensyvyys keskiarvo [cm]', 'Keskituulen nopeus keskiarvo [m/s]']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    # Hae kuukaudet dataframesta
    months = get_months(data)
    
    selected_nodes = st.multiselect('Select a node', available_nodes(), default=3200)
    # Dropdown-valikko kuukausien valitsemiseksi
    selected_month = st.selectbox("Valitse kuukausi:", months)
    # Vaihtoehto kaikkien päivien tai oman päivän valitsemiseksi
    selection_option = st.sidebar.radio("Valitse: ", ("Kaikki päivät", "Yksittäinen päivä"))
    # Otetaan kuukaudet ja lasketaan kuukausien keskiarvot
    month_data = data[data["Kuukausi"] == selected_month]
    month_data_numeric = month_data.select_dtypes(include=[float])
    month_mean = month_data_numeric.mean()
    # Lasketaan aiempien kuukausien keskiarvot
    previous_month = months[months.index(selected_month) - 1]
    previous_month_data = data[data["Kuukausi"] == previous_month]
    previous_month_data_numeric = previous_month_data.select_dtypes(include=[float])
    previous_month_mean = previous_month_data_numeric.mean()
    # Jos valitaan "Kaikki päivät" niin saadaan näkyviin vain kuukauden keskiarvot
    if selection_option == "Kaikki päivät":
        st.write(" ")
        st.markdown('<p class="center big"><b>📊 {} asiakasmäärä & sään keskiarvot 📊</b></p>'.format(selected_month), unsafe_allow_html=True)
        st.write(" ")
        # Lisätään streamlittiin 2 saraketta
        col = st.columns(2)
        with col[1]:
            # Lasketaan erotus nykyisen ja aiemma kuukauden välillä
            temperature_change = round(month_mean['Ilman lämpötila keskiarvo [°C]'] - previous_month_mean['Ilman lämpötila keskiarvo [°C]'], 1)
            humidity_change = round(month_mean['Suhteellinen kosteus keskiarvo [%]'] - previous_month_mean['Suhteellinen kosteus keskiarvo [%]'], 1)
            snow_depth = round(month_mean['Lumensyvyys keskiarvo [cm]'] - previous_month_mean['Lumensyvyys keskiarvo [cm]'], 1)
            rain_change = round(month_mean['Sademäärä keskiarvo [mm]'] - previous_month_mean['Sademäärä keskiarvo [mm]'], 2)
            wind_change = round(month_mean['Keskituulen nopeus keskiarvo [m/s]'] - previous_month_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)
            # Näytetään nykyisen kuukauden tiedot, sekä yllä laskettu erotus + pyöristetään sopivaan lukuun
            with st.container(border=True):
                st.metric("Lämpötilan keskiarvo :thermometer:", f"{np.around(month_mean['Ilman lämpötila keskiarvo [°C]'], 1)} °C", f"{temperature_change} °C")
            with st.container(border=True):
                st.metric("Suhteellisen kosteuden keskiarvo :droplet:", f"{np.around(month_mean['Suhteellinen kosteus keskiarvo [%]'], 1)} %", f"{humidity_change} %")
            with st.container(border=True):
                st.metric("Sademäärän keskiarvo :rain_cloud:", f"{np.around(month_mean['Sademäärä keskiarvo [mm]'], 2)} mm", f"{rain_change} mm")   
            with st.container(border=True):
                st.metric("Keskituulen nopeuden keskiarvo :wind_blowing_face:", f"{np.around(month_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)} m/s", f"{wind_change} m/s") 
            # Jos kuukausi ei ole joku näistä niin lumensyvyys rivi jää pois
            with st.container(border=True):
                if selected_month in ["Tammikuu-2020", "Maaliskuu-2019", "Joulukuu-2019", "Marraskuu-2019"]:
                    st.metric("Lumensyvyyden keskiarvo :snowflake:", f"{np.around(month_mean['Lumensyvyys keskiarvo [cm]'], 1)} cm", f"{snow_depth} cm")   
    
        # Täällä lasketaan kuukausien asiakasmäärät ja luodaan kuvaaja niistä
        with col[0]:
            # Lasketaan kuukauden asiakasmäärä ja näytetään se metricin avulla
            month_customer_count = giga.count_paths(month_data, selected_nodes)
            # Lasketaan verrataan aiempaan kuukauteen
            previous_month_count = giga.count_paths(previous_month_data, selected_nodes)
            month_dif = month_customer_count - previous_month_count
            st.metric("Kuukauden asiakasmäärä:", month_customer_count, month_dif)
            st.write("")
            st.write("")
            # Kuukausien nimet ja lisätään asiakasmäärät oikeisiin kuukausiin
            months_names = ["Maaliskuu-2019", "Huhtikuu-2019", "Toukokuu-2019", "Kesäkuu-2019", "Heinäkuu-2019", "Elokuu-2019", "Syyskuu-2019", "Lokakuu-2019", "Marraskuu-2019", "Joulukuu-2019", "Tammikuu-2020"]
            month_customer_counts = [giga.count_paths(data[data["Kuukausi"] == month], selected_nodes) for month in months_names]
            # Luodaan oma dataframe asiakasmäärille ja kuukausille
            data = {'Kuukausi': months_names, 'Asiakasmäärä': month_customer_counts}
            df = pd.DataFrame(data)
            # Järjestetään ne oikein
            df["Kuukausi"] = pd.Categorical(df["Kuukausi"], categories=months_names, ordered=True)
            df = df.sort_values(by="Kuukausi")
            st.write("*Valittu kuukausi pinkillä värillä*")
            bars = alt.Chart(df).mark_bar().encode(
            x='Kuukausi',
            y='Asiakasmäärä',
            color=alt.condition(
                alt.datum.Kuukausi == selected_month,
                alt.value('#FF91A4'),
                alt.value('#4169E1') 
            )
        )
            st.altair_chart(bars, use_container_width=True)
    else:
        st.write(" ")
        days = sorted(data[data["Kuukausi"] == selected_month]["Päivä"].unique())
        selected_day = st.sidebar.selectbox("Valitse päivä:", days)  # Näytä valittu päivä
        selected_day_data = data[(data["Kuukausi"] == selected_month) & (data["Päivä"] == selected_day)]
        previous_day_data = data[(data["Kuukausi"] == selected_month) & (data["Päivä"] == selected_day - 1)]
        st.markdown('<p class="center big"><b>📊 {}. {} asiakasmäärä & sään keskiarvot 📊</b></p>'.format(selected_day, selected_month), unsafe_allow_html=True)
        st.write(" ")
        with Pool(3) as p:
            df_pool = p.starmap(giga.count_paths, [(selected_day_data, selected_nodes), (previous_day_data, selected_nodes)])
            daily_customer_count = df_pool[0]
            previous_day_count = df_pool[1]

        col = st.columns(2)
        with col[0]:
            day_dif = daily_customer_count - previous_day_count
            st.metric("Päivän asiakasmäärä:", daily_customer_count, day_dif)
            # Luodaan oma dataframe päivittäisille asiakasmäärille
            day_data = {'Päivä': sorted(data[data["Kuukausi"] == selected_month]["Päivä"].unique()), 'Asiakasmäärä': [giga.count_paths(data[(data["Kuukausi"] == selected_month) & (data["Päivä"] == day)], selected_nodes) for day in sorted(data[data["Kuukausi"] == selected_month]["Päivä"].unique())]}
            day_df = pd.DataFrame(day_data)
            # Järjestetään päivät oikein
            day_df = day_df.sort_values(by="Päivä")
            st.write("*Valittu kuukausi pinkillä värillä*")
            bars = alt.Chart(day_df).mark_bar().encode(
                x=alt.X('Päivä', axis=alt.Axis(tickCount=len(day_df))),
                y='Asiakasmäärä',
                color=alt.condition(
                    alt.datum.Päivä == int(selected_day),
                    alt.value('#FF91A4'),
                    alt.value('#4169E1') 
                )
            )
            st.altair_chart(bars, use_container_width=True)
        with col[1]:
            # Lasketaan päivittäiset keskiarvot
            daily_mean = selected_day_data.select_dtypes(include=[float]).mean()
            if not previous_day_data.empty:
                previous_day_mean = previous_day_data.select_dtypes(include=[float]).mean()
                temperature_change = round(daily_mean['Ilman lämpötila keskiarvo [°C]'] - previous_day_mean['Ilman lämpötila keskiarvo [°C]'], 1)
                humidity_change = round(daily_mean['Suhteellinen kosteus keskiarvo [%]'] - previous_day_mean['Suhteellinen kosteus keskiarvo [%]'], 1)
                snow_depth = round(daily_mean['Lumensyvyys keskiarvo [cm]'] - previous_day_mean['Lumensyvyys keskiarvo [cm]'], 1)
                rain_change = round(daily_mean['Sademäärä keskiarvo [mm]'] - previous_day_mean['Sademäärä keskiarvo [mm]'], 2)
                wind_change = round(daily_mean['Keskituulen nopeus keskiarvo [m/s]'] - previous_day_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)
                
                with st.container(border=True):
                    st.metric("Lämpötilan keskiarvo :thermometer:", f"{np.around(daily_mean['Ilman lämpötila keskiarvo [°C]'], 1)} °C", f"{temperature_change} °C")
                with st.container(border=True):
                    st.metric("Suhteellisen kosteuden keskiarvo :droplet:", f"{np.around(daily_mean['Suhteellinen kosteus keskiarvo [%]'], 1)} %", f"{humidity_change} %")
                with st.container(border=True):
                    st.metric("Sademäärän keskiarvo :rain_cloud:", f"{np.around(daily_mean['Sademäärä keskiarvo [mm]'], 2)} mm", f"{rain_change} mm")
                with st.container(border=True):
                    st.metric("Keskituulen nopeuden keskiarvo :wind_blowing_face:", f"{np.around(daily_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)} m/s", f"{wind_change} m/s")
                with st.container(border=True):
                    if selected_month in ["Tammikuu-2020", "Maaliskuu-2019", "Joulukuu-2019", "Marraskuu-2019"]:
                        st.metric("Lumensyvyyden keskiarvo :snowflake:", f"{np.around(daily_mean['Lumensyvyys keskiarvo [cm]'], 1)} cm", f"{snow_depth} cm")
            else:
                with st.container(border=True):
                    st.metric("Lämpötilan keskiarvo :thermometer:", f"{np.around(daily_mean['Ilman lämpötila keskiarvo [°C]'], 1)} °C")
                with st.container(border=True):
                    st.metric("Suhteellisen kosteuden keskiarvo :droplet:", f"{np.around(daily_mean['Suhteellinen kosteus keskiarvo [%]'], 1)} %")
                with st.container(border=True):
                    st.metric("Sademäärän keskiarvo :rain_cloud:", f"{np.around(daily_mean['Sademäärä keskiarvo [mm]'], 2)} mm")
                with st.container(border=True):
                    st.metric("Keskituulen nopeuden keskiarvo :wind_blowing_face:", f"{np.around(daily_mean['Keskituulen nopeus keskiarvo [m/s]'], 1)} m/s")
                with st.container(border=True):
                    if selected_month in ["Tammikuu-2020", "Maaliskuu-2019", "Joulukuu-2019", "Marraskuu-2019"]:
                        st.metric("Lumensyvyyden keskiarvo :snowflake:", f"{np.around(daily_mean['Lumensyvyys keskiarvo [cm]'], 1)} cm")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                # Näytä valitun päivän sää klo 9-21 välillä
        with st.expander("Täältä löytyy tarkempaa tietoa päivän säästä"):
            st.write("*Täältä löytyy säätietoa 9-21 aikaväliltä.*")
            selected_day_data_time = selected_day_data[(selected_day_data["Aika [Paikallinen aika]"] >= "09:00") & (selected_day_data["Aika [Paikallinen aika]"] <= "21:00")]
                
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