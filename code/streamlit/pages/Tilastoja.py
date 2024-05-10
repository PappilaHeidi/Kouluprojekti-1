import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(
    page_title="Muita tilastoja",
    page_icon="📈",
    layout="wide"
)

def read_node(tbl: str, node_name: str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetch_df()
    con.close()
    return df

# Lataa data
@st.cache_data()
def load_data(file: str, tbl: str, node: str):
    df = read_node(tbl, node, file)
    return df

file = "/code/data/duckdb.database"
tbl = "Silver_SensorData"
node = "3200"

tab1, tab2 = st.tabs(["Ajallista tietoa", "Paikannus tietoa"])

# st.title(":chart_with_upwards_trend: Muita tilastoja :chart_with_downwards_trend:")

with tab1:
    st.title(":alarm_clock: Datan ajallista statistiikkaa :stopwatch:")

    col1, col2, col3, col4, col5 = st.columns(5)

    df = load_data(file, tbl, node)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds()
    df = df.dropna()

    mean_dt = df['time_diff'].mean()
    std_dt = df['time_diff'].std()
    median_dt = df['time_diff'].median()
    kurtosis_dt = df['time_diff'].kurtosis()
    skew_dt = df['time_diff'].skew()

    with col1:
        st.info("Keskiarvo | μ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin keskiarvo kertoo keskimääräisen aikaeron peräkkäisten havaintojen välillä.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin keskiarvo:", f"{mean_dt:.2f}s")

    with col2:
        st.info("Keskihajonta | σ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin keskihajonta kertoo näytevälin aikaerojen hajonnan eli vaihtelun määrän.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin keskihajonta:", f"{std_dt:.2f}s")

    with col3:
        st.info("Mediaani | η")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin mediaani kertoo havaintojen keskimmäisen arvon jakaumassa.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin mediaani:", f"{median_dt:.2f}s")

    with col4:
        st.info("Kurtoosi | κ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin Kurtoosi kertoo jakauman huipun muodon terävyyden.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin kurtoosi:", f"{kurtosis_dt:.2f}s")

    with col5:
        st.info("Skewness | γ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin Skewness (vinous) kertoo jakauman vinouden.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin vinous:", f"{skew_dt:.2f}s")
            st.write("")

    col6, col7 = st.columns(2)

    z_scores = (df['time_diff'] - mean_dt) / std_dt
    df['z_score'] = z_scores

    with col6:
        st.title("Outlierit")
        with st.container(border=True):
            st.info("Z-pisteet")
            st.markdown('<span style="color:pink;">Outlierien löytämiseen käytettiin Z-piste kaavaa: z = (x - μ) / σ</span>', unsafe_allow_html=True)
            st.metric("Korkein Z-piste:", f"{z_scores.max():.2f}")
            st.metric("Matalin Z-piste:", f"{z_scores.min():.2f}")

        # Outliereiden laskeminen Z-pisteiden avulla
        outliers = df[np.abs(z_scores) > 3]

        # Scatter plot outliereista
        plt.figure(figsize=(10, 6))
        plt.scatter(df.index, df['time_diff'], color='deepskyblue', label='Data')
        plt.xlabel('Indeksi')
        plt.ylabel('Aikaero (s)')

        # Etsi ja merkitse outliereita
        plt.scatter(outliers.index, outliers['time_diff'], color='lightcoral', label='Outlierit')
        # Lisää viiva oikeaan kohtaan
        plt.axhline(y=mean_dt + 3 * std_dt, color='black', linestyle='-', label='Raja')
        plt.legend()
        st.pyplot(plt)

    st.title("Ajallinen jakautuminen")
    with st.container(border=True):
        st.markdown('<span style="color:pink;">Ajallinen jakautuminen kertoo meille, kuinka monta havaintoa nähdään päivittäin, viikoittain sekä kuukausittain.</span>', unsafe_allow_html=True)

    col8, col9, col10 =st.columns(3)

    # Luodaan kopio DataFramesta, jossa aikaleima on indeksinä
    df_time_index = df.set_index('timestamp')

    with col8:
        # Päivittäinen jakautuminen
        daily_counts = df_time_index.resample('D').size()
        st.progress(0.1)
        plt.figure(figsize=(10, 6))
        plt.plot(daily_counts.index, daily_counts.values, color='deepskyblue', label='Päivittäin')
        plt.xlabel('Päivä')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen päivittäin')
        plt.legend()
        st.pyplot(plt)

    with col9:
        # Viikoittainen jakautuminen
        weekly_counts = df_time_index.resample('W').size()
        st.progress(0.5)
        plt.figure(figsize=(10, 6))
        plt.plot(weekly_counts.index, weekly_counts.values, color='deepskyblue', label='Viikoittain')
        plt.xlabel('Viikko')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen viikoittain')
        plt.legend()
        st.pyplot(plt)

    with col10:
        # Kuukausittainen jakautuminen
        monthly_counts = df_time_index.resample('M').size()
        st.progress(1.0)
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_counts.index, monthly_counts.values, color='deepskyblue', label='Kuukausittain')
        plt.xlabel('Kuukausi')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen kuukausittain')
        plt.legend()
        st.pyplot(plt)

with tab2:
    st.title(":round_pushpin: Datan paikannus statistiikkaa :world_map:")
