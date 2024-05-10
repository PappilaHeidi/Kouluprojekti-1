import streamlit as st
import liike as lk

st.set_page_config(
    page_title="Liikennöinti",
    page_icon=":shopping_trolley:",
    layout="wide"
)

file = "data/duckdb.database"
tbl = "Silver_SensorData"
node = "3200"
df = lk.read_node(tbl, file, node)

st.title(':shopping_trolley: Liikennöinti :shopping_trolley:')

st.markdown(""" Jotain... moi""")

st.title(""" Suositut ajat """)
st.markdown(""" Suosituin aika käydä kaupassa ja viikonpäivä. """)

monthly_counts = lk.count_paths_monthly(df)

st.title("Kuukausittaiset asiakasmäärät")
st.bar_chart(monthly_counts, x=monthly_counts.index.strftime('%Y-%m'), y=monthly_counts.values)
st.xlabel('Kuukausi')
st.ylabel('Asiakasmäärä')

st.title(""" Läpimeno ajat """)
st.markdown(""" Kauanko asiakas viettää kaupassa keskimäärin ja ruuhka ajat. + arvioidaan kassojen määrä. """)