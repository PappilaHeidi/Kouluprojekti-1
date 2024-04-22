import streamlit as st
import duckdb
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title = "Andreaksen GIGAkoodi kärryjenliikkeestä",
    page_icon="💻",
    layout = "wide"
)

st.title('Andreaksen GIGAkoodi')

st.markdown("""
            * Valinta minkä kärryn dataa halutaan kuvata (Dropdown)
            
            * Valinta miltä aikaväliltä halutaan kärryä seurata (Päivä + aika)
            (En ole vielä kovin vartma miten toteutan tämän)
            
            * Valinta tehty, painetaan nappulaa (suoritusnappula)

            * Tulostus valinnoista kaupan mappiin
            """)

# Luetaan data from duckdb.database
def read_node(tbl:str, node_name:str, file: str):
    con = duckdb.connect(database=file)
    df = con.execute(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").fetchdf()
    con.close()
    return df

# Laitetaan tiedostolle oikee path ja valitaan oikea node
file = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..", "data", "duckdb.database"))
tbl = "Silver_SensorData"
node = "3200"
df = read_node(tbl, node, file)

# Function to draw data on the image
def draw_on_image(df):
    img_path = 'kauppa.jpg'
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    
    # Calibration parameters
    x_offset = 111
    y_offset = 23
    x_scale = 1166/10500
    y_scale = 563/5150
    
    def scale_coords(x, y):
        xr = (x * x_scale) + x_offset
        yr = (y * y_scale) + y_offset
        return xr, yr

    for _, row in df.iterrows():
        x, y = scale_coords(row['x'], row['y'])
        draw.rectangle((x, y, x + 2, y + 2), fill='red')
    
    return img

# Streamlit app
st.title('Drawing Testfield Data')

# Display data
st.subheader('Data')
st.write(df)

# Filter and process data
df_lim = df[(df['x'] >= 550)]
df_lim['time_diff'] = df_lim['timestamp'].diff()

iloc_list = []
for index, value in df_lim.iterrows():
    if value['time_diff'] > pd.Timedelta(minutes=5):
        iloc_list.append(index)

paths_values = np.arange(0, len(iloc_list), 1)
for i in range(len(iloc_list) - 1):
    start_index = iloc_list[i]
    end_index = iloc_list[i + 1]
    df_lim.loc[start_index:end_index, "paths"] = paths_values[i]

# Draw data on the image
st.subheader('Draw Data on Image')
img = draw_on_image(df_lim)
st.image(img, caption='Data on Image', use_column_width=True)

# Display number of paths
st.subheader('Number of Paths')
st.write(len(iloc_list) - 1)
