import streamlit as st

st.set_page_config(
    page_title = "Heatmap",
    page_icon="😅",
    layout = "wide"
)

st.title('Heidin GIGAHeatmap')

st.markdown("""
            Kaupanmapin kuumat kohteet tulostettuna lämpimillä ja kylmillä väreillä
            (Tehtävänannossa pyyddetty tekemään eri aikaväleissä, myös viikonpäivinä)""")
