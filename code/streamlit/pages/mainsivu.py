import streamlit as st

st.set_page_config(
    page_title = "Keskivahavat Suorittajat", 
    page_icon="💪",
    layout = "wide"
)

st.title('Keskivahavat Suorittajat')

st.image('5_gubbee.jpg', caption='Me ollaan Suorittajii')

st.header('Linkit:')
st.link_button("Rojektin Gitlab", "https://gitlab.dclabra.fi/andreaskon/projektiopinnot-1-datan-hallinta-ttm23sai")
st.link_button("Rojetktin Blogi", "https://gitlab.dclabra.fi/wiki/F_wwWScxRwi_Hn0esldLIw?view")




st.markdown("""
            
            Tänne joku magee kuva kuvaamaan meidän tiimiä (Joku GigaChad tyylinen(?))

            Joku selostus/larppausjuttu siitä mitä ollaan saatu aikaiseksi
         
            Jotkut loppupuhetyyliset lässynläät Jaakolle ja Pekalle mitä mieltä oltiin tästä rojektista 
    """)