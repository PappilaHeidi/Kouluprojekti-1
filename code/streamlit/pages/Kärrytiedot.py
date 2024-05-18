import streamlit as st
from PIL import Image, ImageDraw, ImageFont
#import ipywidgets as widgets
import matplotlib.pyplot as plt
import gigafunctions as giga
import duckdb as dd
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from multiprocessing import Pool

kuukaudet = [
    "Tammikuu",
    "Helmikuu",
    "Maaliskuu",
    "Huhtikuu",
    "Toukokuu",
    "Kesäkuu",
    "Heinäkuu",
    "Elokuu",
    "Syyskuu",
    "Lokakuu",
    "Marraskuu",
    "Joulukuu"
]

st.set_page_config(
    page_title = "Kärryjen tilastoja",
    page_icon="📈",
    layout = "wide"
)



#Käytä Silver-databasea
tbl = "Silver_SensorData"
col = st.columns((1.5, 10.5, 3.3), gap='medium')

def available_nodes():
    nodes = giga.fetch_nodes() #fetch all nodes in db
    node_list = sorted([int(str(x[0])) for x in nodes])
    return node_list

with st.status("Pieni hetki...", expanded=True) as status:
    st.write("tuodaan dataa tietokannasta")
    if "big_data" not in st.session_state:
        st.session_state.big_data = giga.read_db_to_df(tbl)
    
    st.write("rakennetaan kärryjen tilastoja")
    if "charts" not in st.session_state:
        st.session_state.charts = True
        df_cart_volume_inshop = giga.cart_volume_data(st.session_state.big_data)
        df_cart_volume_charging = giga.cart_volume_data(st.session_state.big_data, area='charging')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_cart_volume_inshop['node_id'], y=df_cart_volume_inshop['y'], name="liikkeessä"))
        fig.add_trace(go.Scatter(x=df_cart_volume_charging['node_id'], y=df_cart_volume_charging['y'], name="latauksessa"), secondary_y=True)
        fig.update_layout(title_text="Kärryjen aktiivisuuden volyymi")
        fig.update_xaxes(title_text="Kärryn id", showgrid=True)
        fig.update_yaxes(title_text="<b>käytössä</b> olevat kärryt", secondary_y=False)
        fig.update_yaxes(title_text="<b>latauksessa</b> olevat kärryt", secondary_y=True)

        #käyttöaste
        df_cart_util = df_cart_volume_inshop.copy()
        df_cart_util['cart_util'] = df_cart_volume_inshop['y'] / df_cart_volume_charging['y']

        fig2 = px.bar(df_cart_util, x='node_id', y='cart_util',
             
             labels={'node_id':'Kärryn id', 'cart_util': 'Käyttöaste -%'}, height=400)
        fig2.update_layout(title_text="Kärryjen käyttöasteet (käytössä/latauksessa)")
        st.session_state.charts = [fig, fig2]

    status.update(label="Lataus valmis!", state="complete", expanded=False)

if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"
    st.session_state.disabled = True

if "kuukausivertailu" not in st.session_state:
    st.session_state.kuukausivertailu = False

if "aikavali" not in st.session_state:
    st.session_state.aikavali = False

if "yksittaiset_reitit" not in st.session_state:
    st.session_state.yksittaiset_reitit = False

if 'plot' not in st.session_state:
    st.session_state.plot = 0

if 'paths' not in st.session_state:
    st.session_state.paths = 0

if 'df_delta' not in st.session_state:
    st.session_state.df_delta = False

# SIVUPALKKI
with st.sidebar: 
    df = st.session_state.big_data
    st.title('Kärrytilasto 📈')
    selected_nodes = st.selectbox('Select a node', available_nodes())
    selected_big_data = st.checkbox('Valitse kaikki kärryt', key='kaikki_karryt')
    st.write(":warning:")
    st.write("Kaikkien kärryjen käsittely kestää pidempään")
    if selected_big_data:
        st.write(":red[Kaikki kärryt valittu]")
    else:
        df = giga.read_db_to_df(tbl, selected_nodes)
    min_date = df['timestamp'].min()
    max_date = df['timestamp'].max()
    months = list(set(df['timestamp'].dt.month.tolist()))
    years = list(set(df['timestamp'].dt.year.tolist()))
    selected_radio = st.radio("Analysointitapa", ["Kuukausivertailu", "Yksittäiset reitit"], index=None, key='sidebar_radio')

    if selected_radio == "Määritä oma aikaväli":
        selected_dates = st.date_input('Valitse aikajakso', value=(min_date, min_date + datetime.timedelta(days=10)), min_value=min_date, max_value=max_date)
        try:
            df_plot = df[df['timestamp'].dt.date.between(*selected_dates)]
            df_paths = giga.read_paths(df_plot)
            path_amount = giga.count_paths(df_paths)
            st.session_state.aikavali = True
        except:
            st.error("Valitse päättymispäivä")
            st.session_state.aikavali = False
        
    if selected_radio=="Kuukausivertailu":
        selected_first_year = st.selectbox("Valitse vuosi", years)
        month = list(set(df[df['timestamp'].dt.year == selected_first_year]['timestamp'].dt.month.tolist()))
        selected_first_month = st.selectbox("Valitse kuukausi", month)
        selected_compared_year = st.selectbox("Valitse vertailtava vuosi", years)
        month2 = list(set(df[df['timestamp'].dt.year == selected_compared_year]['timestamp'].dt.month.tolist()))
        if selected_compared_year == selected_first_year:
            month2.pop(0) #poistaa ensimmäisen kuukauden listasta, jotta sitä ei voi valita vertailtavaksi
        selected_compared_month = st.selectbox("Valitse vertailtava kuukausi", month2)

        if (selected_compared_month <= selected_first_month and selected_first_year == selected_compared_year) or (selected_first_year > selected_compared_year):
            st.error("Väärä valinta")
            st.session_state.kuukausivertailu = False
        else:
            st.session_state.kuukausivertailu = True
            df_start = df[(df['timestamp'].dt.year == selected_first_year) & (df['timestamp'].dt.month == selected_first_month)]
            df_end = df[(df['timestamp'].dt.year == selected_compared_year) & (df['timestamp'].dt.month == selected_compared_month)]
            try:
                #start_time = time.perf_counter()
                #df_start = giga.read_paths(df_start)
                #df_end = giga.read_paths(df_end)
                #multiprocessing
                with Pool(3) as p:
                    df_pool = p.map(giga.read_paths, [df_start, df_end])
                df_start = df_pool[0]
                df_end = df_pool[1]

                #end_time = time.perf_counter()
                #st.write("total:", end_time-start_time)
            except:
                st.error("Reittitietoja ei pystytty hakemaan")
            
            path_amount1 = giga.count_paths(df_start)
            path_amount2 = giga.count_paths(df_end)
            df_start.index = df_start.index.set_levels([df_start.index.levels[0], pd.to_datetime(df_start.index.levels[1])])
            df_end.index = df_end.index.set_levels([df_end.index.levels[0], pd.to_datetime(df_end.index.levels[1])])
            months = list(set(df_end.index.get_level_values(1).month.tolist() + df_start.index.get_level_values(1).month.tolist()))
            kk1 = kuukaudet[months[0]-1]
            kk2 = kuukaudet[months[1]-1]     

    if selected_radio=="Yksittäiset reitit":
        def df_delta():
            st.session_state.df_delta = True

        st.session_state.yksittaiset_reitit = True
        with st.status("Pieni hetki...", expanded=True) as status:
            st.write("kerätään kärryjä")

            status.update(label="Lataus valmis!", state="complete", expanded=False)

        selected_dates = st.date_input('Valitse aikajakso', value=(min_date, min_date + datetime.timedelta(days=10)), min_value=min_date, max_value=max_date, on_change = df_delta)
        if st.session_state.df_delta:
            st.session_state.paths = df[df['timestamp'].dt.date.between(*selected_dates)]
            st.session_state.df_delta = False
        try:
            df_paths = st.session_state.paths
            df_paths = giga.read_paths(df_paths)
            path_amount = giga.count_paths(df_paths)
            st.session_state.aikavali = True
        except:
            st.error("Valitse päättymispäivä")
            st.session_state.aikavali = False
        
# PÄÄSIVU VASEN
with col[0]:
    if selected_radio == "Määritä oma aikaväli" and st.session_state.aikavali:
        st.markdown("#### Käyttö")
        st.metric(label="Yhteensä ", value=f"{path_amount} kpl")
        st.metric(label="joku", value="24")

    if selected_radio=="Kuukausivertailu" and st.session_state.kuukausivertailu:
        st.markdown("#### Kierrokset")
        st.metric(label=kk1, value=f"{path_amount1} kpl")
        st.metric(label=kk2, value=f"{path_amount2} kpl", delta=f"{np.round(((path_amount2-path_amount1)/path_amount1 * 100))} %")
        st.write("")
        st.markdown("#### Päivän keskiarvot")
        st.metric(label=kk1, value=f"{path_amount1//30} kpl")
        st.metric(label=kk2, value=f"{path_amount2//30} kpl")
# PÄÄSIVU KESKI
with col[1]:
    
    if selected_radio == "Määritä oma aikaväli" and st.session_state.aikavali:
        #ei piirretä tähän radioon
        st.image(giga.draw(df_plot))
        st.write("Linechartteja: volyymi(liikenne), asiakkaiden määrä/pvm, säätiedot")
    
    if selected_radio == "Kuukausivertailu" and st.session_state.kuukausivertailu:
        #käyttömäärät
        chart_data = giga.chart_df(df_start, df_end)
        st.area_chart(chart_data, x="Päivät", y=['kk1','kk2'])
        #aktiivisuus
        st.plotly_chart(st.session_state.charts[0],use_container_width=True)
        st.plotly_chart(st.session_state.charts[1], use_container_width=True)

#plottaussivu
def plot_button(df_paths, input_num):
    
    df_level_0_loc = df_paths.index.unique('paths')[input_num]
    df_paths = df_paths.loc[df_level_0_loc]
    st.image(giga.draw(df_paths))

if selected_radio == "Yksittäiset reitit" and st.session_state.aikavali:
    st.markdown("# Seuraa kierroksia pohjakuvasta")
    
    plot_input = st.number_input("Seuraava reitti", value = 1, min_value = 1, max_value = path_amount)
    col2, col3, col4 = st.columns(3, gap='small')
    df_timedelta = df_paths.index.get_level_values('timestamp')
    time_spent = df_timedelta.max() - df_timedelta
    df_paths_paths = df_paths.reset_index()
    min_time = df_paths_paths.groupby('paths')['timestamp'].min()
    max_time = df_paths_paths.groupby('paths')['timestamp'].max()
    df_path_timedelta = max_time - min_time
    df_path_timedelta = pd.DataFrame(df_path_timedelta)
    df_path_timedelta['seconds'] = df_path_timedelta['timestamp'].dt.total_seconds()
    path_avg = df_path_timedelta['timestamp'].mean()
    int_value_minutes_avg = round(int(path_avg.total_seconds()) / 60, 0)
    df_path_timedelta['int_timedelta'] = (df_path_timedelta['timestamp'].dt.total_seconds() / 60).round(0)
    df_path_timedelta = df_path_timedelta.reset_index()
    
    with col2:
        st.metric(label="Asiakkaita yht.", value=f"{path_amount} kpl")
    with col3:
        if st.session_state.kaikki_karryt:
            st.metric(label="Kierrosten keskiarvo", value=f'{int_value_minutes_avg//len(available_nodes())} min')
        else: 
            st.metric(label="Kierrosten keskiarvo", value=f'{int_value_minutes_avg} min')

    with col4:
        st.metric(label="Nykyinen kierrosaika", value=f"{df_path_timedelta['int_timedelta'][plot_input-1]} min")
    
    plot_button(df_paths, plot_input)

    with st.expander('Lisätietoja', expanded=True):
        st.write('''
            - Data: [Iiwari Tracking Solutions](<https://www.iiwari.com/>).
            - :red[**Asiakasmäärät**]: Ajanjakson aikaiset ja kärrykohtaiset asiakasmäärät
                 - Asiakasmäärät on laskettu hakemalla aluksi välimuistissa oleva dataframe-olio ja käyttämällä se read_paths() -> _cash_pipe() -> count_paths()-funktioissa.
                 reittien laskufunktio hakee reittien alkamis- ja päättymispisteet ja palauttaa suodatetun dataframen uusilla indekseillä ja sarakkeilla. Tämän jälkeen asiakasmääriä
                 voi kysellä count_paths() funktiossa. count_paths()-funktio hyväksyy myös vieraita dataframe-olioita, jos tietty notaatio täsmää.
            - :red[**Kierrosten keskiarvo**]: Valitun ajanjakson ja asiakkaiden myymälässä vietetyn ajan keskiarvo
                 - Keskiarvo on saatu laskemalla valittujen kärryjen kierrosaika myymälässä, jaettuna kyseisillä kärryillä
            - :red[**Nykyinen kierrosaika**]: Kartalla näkyvän kierroksen pituus minuutteina
                 - Keskiarvot ja kierrosten ajat on saatu samasta dataframesta ryhmittämällä reitti-indeksit ja laskemalla max-min-erotus ja muuttamalla datetime sekunnit int-minuuteiksi
            - :red[**Datapisteet**]: Asiakkaan kävelyreitti porteilta, kassalle
                 ''')    

#PÄÄSIVU OIKEA
with col[2]:
    if selected_radio == "Määritä oma aikaväli" and st.session_state.aikavali:
        st.write("dataframe ja about")

    if selected_radio == "Kuukausivertailu" and st.session_state.kuukausivertailu:
        st.markdown('#### Asiakasmäärät')

        st.dataframe(chart_data,
                    column_order=("Päivät", "kk1", "kk2"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "day": st.column_config.TextColumn(
                            "Päivät",
                        ),
                        "kk1": st.column_config.ProgressColumn(
                            kk1,
                            format="%f",
                            min_value=0,
                            max_value=max(chart_data['kk1']),
                        ),
                        "kk2": st.column_config.ProgressColumn(
                            kk2,
                            format="%f",
                            min_value=0,
                            max_value=max(chart_data['kk2']),
                        )}
                    )
        
        with st.expander('Lisätietoja', expanded=True):
            st.write('''
                - Data: [Iiwari Tracking Solutions](<https://www.iiwari.com/>).
                - :orange[**Kierrokset**]: Kärryillä kuljetut asiakkaiden kierrosten määrät kaupan sisällä / valittu kuukausi
                - :orange[**Asiakasmäärät**]: Asiakasmäärien vertailu kuukausittain. Päivät vastaavat samoja kuukauden päiviä
                - :orange[**Aktiivisuus**]: Kärryjen aktiivisuus on UWB-paikannusjärjestelmän vastaanottamaa signaalia kärryiltä
                - :orange[**Käyttöaste**]: Kärryjen käyttöaste on niiden käyttöaika suhteessa latausaikaan
                     ''')

