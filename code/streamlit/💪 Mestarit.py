import streamlit as st
import base64

st.set_page_config(
    page_title = "Keskivahavat Suorittajat", 
    page_icon="💪🏼",
    layout = "wide"
)

st.title('✨ Keskivahavat Suorittajat ✨')

st.image('5_gubbee.jpg', caption='Me ollaan Suorittajii')
st.write("---")

st.header('Linkit:')
st.link_button("Rojektin Gitlab", "https://gitlab.dclabra.fi/andreaskon/projektiopinnot-1-datan-hallinta-ttm23sai")
st.link_button("Rojektin Blogi", "https://gitlab.dclabra.fi/wiki/F_wwWScxRwi_Hn0esldLIw?view")
# Käytä iframea upottaaksesi sivusto Streamlittiin
st.markdown('<iframe src="https://app.clockify.me/shared/6638f3a1963af9639f17dfb0" width="1000" height="600"></iframe>', unsafe_allow_html=True)
st.write("---")

st.markdown("""
            
            Tänne joku magee kuva kuvaamaan meidän tiimiä (Joku GigaChad tyylinen(?))

            Joku selostus/larppausjuttu siitä mitä ollaan saatu aikaiseksi
         
            Jotkut loppupuhetyyliset lässynläät Jaakolle ja Pekalle mitä mieltä oltiin tästä rojektista 
    """)

st.write("---")

st.write("**(live footage of us doing the project)**")
gif_link = "https://giphy.com/embed/ukMiDlCmdv2og"
st.markdown(f'<iframe src="{gif_link}" width="490" height="367" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
