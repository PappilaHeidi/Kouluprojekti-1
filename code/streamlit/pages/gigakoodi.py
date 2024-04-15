import streamlit as st
import duckdb as dd
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

st.set_page_config(
    page_title = "Andreaksen GIGAkoodi kärryjenliikkeestä",
    page_icon="💻",
    layout = "wide"
)

st.title('Andreaksen GAkoodi')

st.markdown("""
            * Valinta minkä kärryn dataa halutaan kuvata (Dropdown)
            
            * Valinta miltä aikaväliltä halutaan kärryä seurata (Päivä + aika)
            (En ole vielä kovin vartma miten toteutan tämän)
            
            * Valinta tehty, painetaan nappulaa (suoritusnappula)

            * Tulostus valinnoista kaupan mappiin
            """)



# Read data from DuckDB
def read_node(tbl, node):
    conn = dd.connect(database='Silver_SensorData')
    query = "SELECT * FROM Silver_SensorData WHERE node_id = 3200"
    df = conn.execute(query).fetch_df()
    return df

# Function to draw data on the image
def draw_on_image(df):
    img_path = '../code/kauppa.jpg/'
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

# Read data
tbl = "Silver_SensorData"
node = "3200"
df = read_node(tbl, node)

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
