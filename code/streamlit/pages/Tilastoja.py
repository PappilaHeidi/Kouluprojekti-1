import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure
from scipy.stats import norm

st.set_page_config(
    page_title="Muita tilastoja",
    page_icon="📈",
    layout="wide"
)

#Luetaan tietokanta
def read_node(tbl: str, node_name: str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetch_df()
    con.close()
    return df

#Ladataan data
@st.cache_data()
def load_data(file: str, tbl: str, node: str):
    df = read_node(tbl, node, file)
    return df

#Valitaan oikea table yms...
file = "/code/data/duckdb.database"
tbl = "Silver_SensorData"
node = "3200"
#node = st.sidebar.selectbox("Valitse node:", ["3200", "3224", "3240", "42787", "45300", "51719", "51720", "51735", "51751", "51850", "51866", "51889", "51968", "51976", "51992", "52003", "52008", "52023", "52099", "52535", "53000", "53011", "53027", "53130", "53768", "53795", "53888", "53924", "53936", "54016", "64458"])

#Lisätään sivut
tab1, tab2 = st.tabs(["Ajallista tietoa", "Paikannus tietoa"])

# st.title(":chart_with_upwards_trend: Muita tilastoja :chart_with_downwards_trend:")

#Muutetaan oikeaan muotoon
df = load_data(file, tbl, node)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['time_diff'] = df['timestamp'].diff().dt.total_seconds()
df = df.dropna()

#Lasketaan ajan stats
mean_dt = df['time_diff'].mean()
std_dt = df['time_diff'].std()
median_dt = df['time_diff'].median()
kurtosis_dt = df['time_diff'].kurtosis()
skew_dt = df['time_diff'].skew()
max_dt = df['time_diff'].max()
min_dt = df['time_diff'].min()

#Lasketaan X stats
x_mean = df['x'].mean()
x_std = df['x'].std()
x_median = df['x'].median()
x_kurtosis = df['x'].kurtosis()
x_skew = df['x'].skew()
x_max = df['x'].max()
x_min = df['x'].min()

#Lasketaan Y stats
y_mean = df['y'].mean()
y_std = df['y'].std()
y_median = df['y'].median()
y_kurtosis = df['y'].kurtosis()
y_skew = df['y'].skew()
y_max = df['y'].max()
y_min = df['y'].min()

#kynnysarvo(x) = keskiarvo(x) ± 3 * keskihajonta(x)
#kynnysarvo(𝑥)= 1079.37 ± 3 * 2301.42
#kynnysarvo(x)= −5424.89 ja 7583.63

#kynnysarvo(y) = keskiarvo(y) ± 3 * keskihajonta(y)
#kynnysarvo(𝑦) = 2557.05 ± 3 * 743.37
#kynnysarvo(y) = 328.94 ja 4802.16

#Lasketaan tällä x-kordinaatin outliereiden esiintymistaajuus
x_coords = df['x']
lower_threshold_x = -5424.89
upper_threshold_x = 7583.63
outliers_x = [x for x in x_coords if x < lower_threshold_x or x > upper_threshold_x]
outliers_count_x = len(outliers_x)

total_points_x = len(df['x'])
outliers_frequency_x = (outliers_count_x / total_points_x) * 100

#Lasketaan tällä y-kordinaatin outliereiden esiintymistaajuus
y_coords = df['y']
lower_threshold_y = 328.94
upper_threshold_y = 4802.16
outliers_y = [y for y in y_coords if y < lower_threshold_y or y > upper_threshold_y]
outliers_count_y = len(outliers_y)

total_points_y = len(df['y'])
outliers_frequency_y = (outliers_count_y / total_points_y) * 100

#Lasketaan Y:n kohina
noise_y = np.random.normal(0, y_std, len(df))
df['y_noise'] = df['y'] + noise_y
y_min_noise = df['y_noise'].min()
y_max_noise = df['y_noise'].max()

#Lasketaan X:n kohina
noise_x = np.random.normal(0, x_std, len(df))
df['x_noise'] = df['x'] + noise_x
x_min_noise = df['x_noise'].min()
x_max_noise = df['x_noise'].max()

with tab1:
    st.title(":alarm_clock: Datan ajallista statistiikkaa :stopwatch:")

    #Luodaan sarakkeet
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.info("Maksimi | max")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin maksimi kertoo suurimman muutoksen havaintojen välillä.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin maksimi:", f"{max_dt:.2f}s")

    with col2:
        st.info("Minimi | min")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Näytevälin minimi kertoo pienimmän muutoksen havaintojen välillä.</span>', unsafe_allow_html=True)
            st.metric("Näytevälin minimi:", f"{min_dt:.2f}s")

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

    #Luodaan kuvaaja ajallisesta jakautumisesta
    st.title("Ajallinen jakautuminen")
    with st.container(border=True):
        st.markdown('<span style="color:pink;">Ajallinen jakautuminen kertoo meille, kuinka monta havaintoa nähdään päivittäin, viikoittain sekä kuukausittain.</span>', unsafe_allow_html=True)

    col6, col7, col8 =st.columns(3)

    #Aikaleima indeksinä
    df_time_index = df.set_index('timestamp')

    with col6:
        # Päivittäinen jakautuminen
        daily_counts = df_time_index.resample('D').size()
        st.progress(0.1)
        plt.figure(figsize=(10, 6))
        plt.plot(daily_counts.index, daily_counts.values, color='deepskyblue', label='Päivittäin')
        plt.xlabel('Päivä')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen päivittäin')
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(plt)

    with col7:
        # Viikoittainen jakautuminen
        weekly_counts = df_time_index.resample('W').size()
        st.progress(0.5)
        plt.figure(figsize=(10, 6))
        plt.plot(weekly_counts.index, weekly_counts.values, color='deepskyblue', label='Viikoittain')
        plt.xlabel('Viikko')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen viikoittain')
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(plt)

    with col8:
        # Kuukausittainen jakautuminen
        monthly_counts = df_time_index.resample('ME').size()
        st.progress(1.0)
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_counts.index, monthly_counts.values, color='deepskyblue', label='Kuukausittain')
        plt.xlabel('Kuukausi')
        plt.ylabel('Havaintojen lukumäärä')
        plt.title('Ajallinen jakautuminen kuukausittain')
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(plt)

    col9, col10 = st.columns(2)

    #Luodaan kuvaaja normaalijakaumasta
    with col10:
        st.title("Normaalijakauma")
        with st.container(border=True):
            st.info("Keskiarvo ja keskihajonta")
            st.markdown('<span style="color:pink;">Näytevälin keskiarvo kertoo keskimääräisen aikaeron peräkkäisten havaintojen välillä.</span>', unsafe_allow_html=True)
            st.metric("Keskiarvo | μ", f"{mean_dt:.2f}s")
            st.markdown('<span style="color:pink;">Näytevälin keskihajonta kertoo näytevälin aikaerojen hajonnan eli vaihtelun määrän.</span>', unsafe_allow_html=True)
            st.metric("Keskihajonta | σ", f"{std_dt:.2f}s")

        #Lasketaan normaalijakauma
        x = np.linspace(mean_dt - 4*std_dt, mean_dt + 4*std_dt, 1000)
        y = norm.pdf(x, mean_dt, std_dt)

        #Käytetään Bokeh kirjastoa
        p = figure(x_axis_label='Aikaero (s)', y_axis_label='Tiheys')
        p.line(x, y, line_width=2, color='deepskyblue')
        st.bokeh_chart(p, use_container_width=True)

    #Lasketaan outlierit z-pisteitä käyttäen
    z_scores = (df['time_diff'] - mean_dt) / std_dt
    df['z_score'] = z_scores

    #Luo kuvaajan outliereistä
    with col9:
        st.title("Outlierit")
        with st.container(border=True):
            st.info("Z-pisteet")
            st.markdown('<span style="color:pink;">Outlierien löytämiseen käytettiin Z-piste kaavaa: z = (x - μ) / σ.</span>', unsafe_allow_html=True)
            st.metric("Korkein Z-piste", f"{z_scores.max():.2f}")
            st.metric("Matalin Z-piste", f"{z_scores.min():.2f}")

        #Z-pisteiden absoluuttinen pistemäärä suurempi kuin 3
        outliers = df[np.abs(z_scores) > 3]

        #Scatter plot
        plt.figure(figsize=(10, 9))
        plt.scatter(df.index, df['time_diff'], color='deepskyblue', label='Data')
        plt.xlabel('Indeksi')
        plt.ylabel('Aikaero (s)')

        #Merkitään outlierit
        plt.scatter(outliers.index, outliers['time_diff'], color='lightcoral', label='Outlierit')

        #Määritetään viiva datan ja outlierien väliin
        plt.axhline(y=mean_dt + 3 * std_dt, color='purple', linestyle='-', label='Raja')
        plt.legend()
        st.pyplot(plt)

with tab2:
    st.title(":round_pushpin: Datan paikannus statistiikkaa :world_map:")

    #Luodaan taas sarakkeet
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.info("Keskiarvo | μ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">X-kordinaatin keskiarvo antaa keskimääräisen sijainnin X-akselilla.</span>', unsafe_allow_html=True)
            st.metric("X-kordinaatin", f"{x_mean:.2f}")

    with col2:
        st.info("Keskihajonta | σ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">X-kordinaatin keskihajonta mittaa X-arvojen hajontaa.</span>', unsafe_allow_html=True)
            st.metric("X-kordinaatin", f"{x_std:.2f}")

    with col3:
        st.info("Mediaani | η")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">X-kordinaatin mediaani kertoo keskimmäisen X-arvon.</span>', unsafe_allow_html=True)
            st.metric("X-kordinaatin", f"{x_median:.2f}")

    with col4:
        st.info("Kurtoosi | κ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">X-kordinaatin kurtoosi kuvaa X-arvojen jakauman muotoa.</span>', unsafe_allow_html=True)
            st.metric("X-kordinaatin", f"{x_kurtosis:.2f}")

    with col5:
        st.info("Skewness | γ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">X-kordinaatin vinous kuvaa X-arvojen jakauman vinoutta.</span>', unsafe_allow_html=True)
            st.metric("X-kordinaatin", f"{x_skew:.2f}")
    
    col6, col7, col8, col9, col10 = st.columns(5)

    with col6:
        st.info("Keskiarvo | μ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Y-kordinaatin keskiarvo antaa keskimääräisen sijainnin Y-akselilla.</span>', unsafe_allow_html=True)
            st.metric("Y-kordinaatin", f"{y_mean:.2f}")
    
    with col7:
        st.info("Keskihajonta | σ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Y-kordinaatin keskihajonta mittaa Y-arvojen hajontaa</span>', unsafe_allow_html=True)
            st.metric("Y-kordinaatin", f"{y_std:.2f}")

    with col8:
        st.info("Mediaani | η")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Y-kordinaatin mediaani kertoo keskimmäisen Y-arvon.</span>', unsafe_allow_html=True)
            st.metric("Y-kordinaatin", f"{y_median:.2f}")

    with col9:
        st.info("Kurtoosi | κ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Y-kordinaatin kurtoosi kuvaa X-arvojen jakauman muotoa.</span>', unsafe_allow_html=True)
            st.metric("Y-kordinaatin", f"{y_kurtosis:.2f}")

    with col10:
        st.info("Skewness | γ")
        with st.container(border=True):
            st.markdown('<span style="color:pink;">Y-kordinaatin vinous kuvaa X-arvojen jakauman vinoutta.</span>', unsafe_allow_html=True)
            st.metric("Y-kordinaatin", f"{y_skew:.2f}")

    col11, col12 = st.columns(2)

    #Tehdään outlier kuvaaja x:lle
    with col11:
        st.title("X-kordinaatin outlierit")
        with st.container(border=True):
            st.info("Z-pisteet")
            st.markdown('<span style="color:pink;">Kuvaaja tehty Z-piste kaavaa käyttäen: z = (x - μ) / σ.</span>', unsafe_allow_html=True)
            st.metric("Ulkopuolella olevien pisteiden määrä:", f"{outliers_count_x}")
            st.markdown('<span style="color:pink;">Esiintymistaajuus laskettu: (outlierien määrä / x-kordinaattien kokonaismäärä) * 100%.</span>', unsafe_allow_html=True)
            st.metric("Outliereiden esiintymistaajuus:", f"{outliers_frequency_x:.2f}%")

        #Lasketaan outlierit z-pisteitä käyttäen x-kordinaatille
        x_z_scores = (df['x'] - df['x'].mean()) / df['x'].std()
        df['x_z'] = x_z_scores

        #Z-pisteiden absoluuttinen pistemäärä suurempi kuin 3
        outliers_x = df[np.abs(x_z_scores) > 3]

        #Scatter plot
        plt.figure(figsize=(10, 9))
        plt.scatter(df.index, df['x_z'], color='deepskyblue', label='Data')
        plt.scatter(outliers_x.index, outliers_x['x_z'], color='lightcoral', label='Outlierit')
        plt.axhline(y=3, color='purple', linestyle='-', label='Yläaja')
        plt.axhline(y=-3, color='purple', linestyle='-', label='Alaraja')
        plt.xlabel('Indeksi')
        plt.ylabel('Z-score X')
        plt.title('Scatter plot X-koordinaateille')
        plt.legend()
        st.pyplot(plt)

    #Tehdään outlier kuvaaja y:lle
    with col12:
        st.title("Y-kordinaatin outlierit")
        with st.container(border=True):
            st.info("Z-pisteet")
            st.markdown('<span style="color:pink;">Kuvaaja tehty Z-piste kaavaa käyttäen: z = (x - μ) / σ.</span>', unsafe_allow_html=True)
            st.metric("Ulkopuolella olevien pisteiden määrä:", f"{outliers_count_y}")
            st.markdown('<span style="color:pink;">Esiintymistaajuus laskettu: (outlierien määrä / y-kordinaattien kokonaismäärä) * 100%.</span>', unsafe_allow_html=True)
            st.metric("Outliereiden esiintymistaajuus:", f"{outliers_frequency_y:.2f}%")

        #Lasketaan outlierit z-pisteitä käyttäen x-kordinaatille
        y_z_scores = (df['y'] - df['y'].mean()) / df['y'].std()
        df['y_z'] = y_z_scores

        #Z-pisteiden absoluuttinen pistemäärä suurempi kuin 3
        outliers_y = df[np.abs(y_z_scores) > 3]

        #Scatter plot
        plt.figure(figsize=(10, 9))
        plt.scatter(df.index, df['y_z'], color='deepskyblue', label='Data')
        plt.scatter(outliers_y.index, outliers_y['y_z'], color='lightcoral', label='Outlierit')
        plt.axhline(y=3, color='purple', linestyle='-', label='Yläraja')
        plt.axhline(y=-3, color='purple', linestyle='-', label='Alaraja')
        plt.xlabel('Indeksi')
        plt.ylabel('Z-score Y')
        plt.title('Scatter plot Y-koordinaateille')
        plt.legend()
        st.pyplot(plt)

    col13, col14 = st.columns(2)

    #Tehdään kohinan kuvaaja x:lle
    with col13:
        st.title("X-kordinaatin kohina")
        with st.container(border=True):
            st.info("X-pisteet")
            st.markdown('<span style="color:pink;">Kohina on satunnaista vaihtelua datassa, joka simuloi esimerkiksi epätarkkuuksia.</span>', unsafe_allow_html=True)
            st.metric("Suurin X-kordinaatti:", f"{x_max}")
            st.metric("Pienin X-kordinaatti:", f"{x_min}")
            st.metric("Suurin kohinan X-kordinaatti:", f"{x_max_noise:.0f}")
            st.metric("Pienin kohinan X-kordinaatti:", f"{x_min_noise:.0f}")

        #Luodaan kuvaaja
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['x'], label='Alkuperäiset X-pisteet', color='deepskyblue', linestyle='-')
        plt.plot(df.index, df['x_noise'], label='X-pisteet kohinan kanssa', color='lightcoral', alpha=0.7, linestyle='--')
        plt.xlabel('Indeksi')
        plt.ylabel('X-koordinaattit')
        plt.axhline(y=x_max_noise, color='purple', linestyle='-', label='Ylärajan kohina')
        plt.axhline(y=x_min_noise, color='purple', linestyle='-', label='Alarajan kohina')
        plt.title('Alkuperäiset X-pisteet vs. X-pisteet kohinan kanssa')
        plt.legend()
        st.pyplot(plt)

    #Tehdään kohinan kuvaaja y:lle
    with col14:
        st.title("Y-kordinaatin kohina")
        with st.container(border=True):
            st.info("Y-pisteet")
            st.markdown('<span style="color:pink;">Kohina on satunnaista vaihtelua datassa, joka simuloi esimerkiksi epätarkkuuksia.</span>', unsafe_allow_html=True)
            st.metric("Suurin Y-kordinaatti:", f"{y_max}")
            st.metric("Pienin Y-kordinaatti:", f"{y_min}")
            st.metric("Suurin kohinan Y-kordinaatti:", f"{y_max_noise:.0f}")
            st.metric("Pienin kohinan Y-kordinaatti:", f"{y_min_noise:.0f}")

        #Luodaan kuvaaja
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['y'], label='Alkuperäiset Y-pisteet', color='deepskyblue', linestyle='-')
        plt.plot(df.index, df['y_noise'], label='Y-pisteet kohinan kanssa', color='lightcoral', alpha=0.7, linestyle='--')
        plt.xlabel('Indeksi')
        plt.ylabel('Y-koordinaattit')
        plt.axhline(y=y_max_noise, color='purple', linestyle='-', label='Ylärajan kohina')
        plt.axhline(y=y_min_noise, color='purple', linestyle='-', label='Alarajan kohina')
        plt.title('Alkuperäiset Y-pisteet vs. Y-pisteet kohinan kanssa')
        plt.legend()
        st.pyplot(plt)
