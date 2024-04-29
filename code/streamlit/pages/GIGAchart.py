import streamlit as st
from PIL import Image, ImageDraw, ImageFont
#import ipywidgets as widgets
import matplotlib.pyplot as plt
import gigafunctions as giga
import duckdb as dd
import datetime
import pandas as pd
import numpy as np


st.set_page_config(
    page_title = "Gigachart",
    page_icon="📈",
    layout = "wide"
)


st.sidebar.markdown("Sivupalkki")
#Käytä Silver-databasea
tbl = "Silver_SensorData"
col = st.columns((1.5, 10.5, 2), gap='medium')

if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"
    st.session_state.disabled = True

if "kuukausivertailu" not in st.session_state:
    st.session_state.kuukausivertailu = False


with st.sidebar:
    st.title('GIGAcharts 📈')
    nodes = giga.fetch_nodes() #fetch all nodes in db
    

    
    
    node_list = nodes[0]
    selected_nodes = st.selectbox('Select a node', node_list)
    df = giga.read_db_to_df(tbl, selected_nodes)
    min_year = df['timestamp'].min()
    max_year = df['timestamp'].max()
    months = list(set(df['timestamp'].dt.month.tolist()))
    years = list(set(df['timestamp'].dt.year.tolist()))
    selected_radio = st.radio("Analysointitapa", ["Määritä oma aikaväli", "Kuukausivertailu", "Päivävertailu", "Yksittäiset reitit"], index=None)

    if selected_radio == "Määritä oma aikaväli":
        selected_dates = st.date_input('Select dates', value=(min_year, min_year + datetime.timedelta(days=1)), min_value=min_year, max_value=max_year)
        try:
            df_plot = df[df['timestamp'].dt.date.between(*selected_dates)]
            df_paths = giga.read_paths(df_plot)
            path_amount = giga.count_paths(df_paths)
        except:
            st.error("Valitse päättymispäivä")
    
    if selected_radio=="Kuukausivertailu":
        selected_first_year = st.selectbox("Select first year", years)
        selected_first_month = st.selectbox("Select first month", months)
        selected_compared_month = st.selectbox("Select month to compare", months)
        selected_compared_year = st.selectbox("Select compared year", years)
        if (selected_compared_month <= selected_first_month and selected_first_year == selected_compared_year) or (selected_first_year > selected_compared_year):
            st.error("Väärä valinta")
        else:
            df_start = df[(df['timestamp'].dt.year == selected_first_year) & (df['timestamp'].dt.month == selected_first_month)]
            df_end = df[(df['timestamp'].dt.year == selected_compared_year) & (df['timestamp'].dt.month == selected_compared_month)]
            df_start = giga.read_paths(df_start)
            df_end = giga.read_paths(df_end)
            path_amount1 = giga.count_paths(df_start)
            path_amount2 = giga.count_paths(df_end)
            st.session_state.kuukausivertailu = True
            st.session_state.disabled = False


    #selected_year = st.selectbox('Select a year', year_list, index=None)
    


  

    

with col[0]:
    st.markdown("#### Kierrokset")
    if selected_radio == "Määritä oma aikaväli":
        st.metric(label="Yhteensä ", value=f"{path_amount} kpl")
        st.metric(label="Kierroksen keskiarvo", value="24")
    if selected_radio == "Kuukausivertailu" and st.session_state.kuukausivertailu:
        st.metric(label="Kuukausi 1", value=f"{path_amount1} kpl")
        st.metric(label="Kuukausi 2", value=f"{path_amount2} kpl", delta=f"{np.round(((path_amount2-path_amount1)/path_amount1 * 100))} %")



with col[1]:
    if selected_radio == "Määritä oma aikaväli":
        if len(selected_dates) == 1:
            st.error("Valitse päättymispäivä")
        else:
            #ei piirretä tähän radioon
            st.image(giga.draw(df_plot))
            #heatmap = plotlit.make_heatmap(df_plot, 'timestamp', 'timestamp', '', 'blues')
            #st.altair_chart(heatmap, use_container_width=True)
    
    if selected_radio == "Kuukausivertailu" and st.session_state.kuukausivertailu:
        chart_data = giga.chart_df(df_start, df_end)
        st.area_chart(chart_data, x="day", y=['kk1','kk2'])
        st.write(chart_data)

        
      


