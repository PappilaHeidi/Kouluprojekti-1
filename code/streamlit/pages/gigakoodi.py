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

st.title('Andreaksen GIGAkoodi')

st.markdown("""
            * Valinta minkä kärryn dataa halutaan kuvata (Dropdown)
            
            * Valinta miltä aikaväliltä halutaan kärryä seurata (Päivä + aika)
            (En ole vielä kovin vartma miten toteutan tämän)
            
            * Valinta tehty, painetaan nappulaa (suoritusnappula)

            * Tulostus valinnoista kaupan mappiin
            """)



# Poistin koodin täältä sillä se ei toiminut + Andreas on tehnyt GIGAcharts