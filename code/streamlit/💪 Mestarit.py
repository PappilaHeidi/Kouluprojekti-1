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

st.header('📜 Suorittajien Seikkailu 📜')
st.markdown("""
    

    Projekti alkoi tiimin kokoontuessa yhteen ensimmäisen projektin aloitusluennon jälkeen. Tutustumisleikkien jälkeen roolit määriteltiin, ja alun perin tarkoituksena oli sekoittaa roolipakkaa viikoittain. Sprinttien edetessä kuitenkin huomattiin, että paras lopputulos saavutettaisiin pitämällä rakenteista kiinni. Näin roolit pysyivät alusta loppuun samoina.

    **Tuoteomistaja Andreas** määritteli projektin tavoitteet, asetti kirkkaan päämäärän ja keräsi vaatimukset tuotteen kehitysjonoon. 
            
    **Kehittäjät Joni, Heidi ja Mirva** kokosivat työkalunsa ja yhdistivät viisaat päänsä. Jokaisella oli oma erikoisalansa: 

    - **Joni** vastasi fronttidevaamisesta, kaunistaen projektia väreillä ja nappuloilla.
    - **Heidi** toimi bäkkärinä, huolehtien datan oikeellisuudesta ja erilaisista käyristä.
    - **Mirva** oli moniosaaja, vastuussa projektin turvallisuudesta sekä koodin oikeudellisuudesta ja vastuullisuudesta.

    **Scrum Master Linnea** tuki tiimiä ja varmisti, että Scrum-prosessi toimi saumattomasti. Linnea, jolla oli kokemusta junnudevaajan roolista, ylennettiin tässä projektissa senioriksi. Hän mentoroi junioreja kuin delfiini tiimimme meressä: liitäen aaltojen yllä, tunnustellen esteitä etukäteen ja ohjaten tiimin turvallisesti kohti tavoitetta. Projektissamme tuoteomistaja ja scrum master olivat myös hands-on mukana devaamisessa.

    Sprinttien aikana tiimi työskenteli tiiviisti yhdessä. Vaikka päivittäispalavereita ei voitu pitää, joka toki rikkoi Scrumin pelisääntöjä, asiat käytiin hyvässä hengessä läpi Discossa. Edistymistä seurattiin chateissa ja ongelmat ratkottiin sprinttien aikana. Sprintin lopuksi tiimi kokoontui yhteen käsittelemään Scrumin seremonioita: backlog refinement, planning, review ja retrot. Sprintin päätteeksi esiteltiin valmis inkrementti katselmoijalle, joka antoi palautetta, ja tarvittavat muutokset tehtiin ennen kuin inkrementti julkaistiin tuotantoympäristöön – jos julkaistiin.

    ### Vahvuuksia 💪

    - **Hyvä fiilis:** Tiimihenki pysyi korkealla koko projektin ajan.
    - **Hyvät tyypit:** Jokainen tiimin jäsen toi oman vahvan panoksensa projektiin.
    - **Koodaamisen ilo:** Yhteistyö ja luova ongelmanratkaisu synnyttivät aitoa iloa.
    - **Viikottainen demoilu:** Jatkuvat esittelyt pitivät tiimin fokusoituneena ja motivoituneena.

    ### Heikkouksia 😰

    - **Gitlabin käyttö:** Monille meistä Gitlab oli hieman hämärän peitossa. Issuet, taskit ja linkitetyt itemit menivät usein sekaisin.
    - **Dailyt puuttuivat:** Päivittäisten kohtaamisten puuttuminen rikkoi Scrumin perusperiaatteita.
    - **Milestones:** Milestonesin tekemättömät taskit ja issuet aiheuttivat ongelmia.
    - **Raportointi ja kehitysjonon priorisointi:** Näissä olisi ollut parantamisen varaa.

    ### Projektin Retro 📝

    - **Issuet backlog-itemeinä:** Issuet olisivat voineet toimia paremmin product backlog itemeinä, ja sprint backlogin taskeina.
    - **Taskien kerääminen etukäteen:** Taskit olisi kannattanut kerätä valmiiksi backlogiin sprint-meetingeissä, eikä vasta sprintin aikana.
    - **Lyhyt kirjallinen selitys:** Valmistuneen tuotteen kehitysjonosta olisi voinut tehdä lyhyen kirjallisen selityksen.
    - **Storypointit:** Storypointtien (Gitlab weight) käyttöä olisi pitänyt parantaa.

    ### Lopputulos 🏁

    Projekti päättyi onnistuneesti ja saimme arvokasta oppia Scrumista ja DevOpsista käytettyyn aikaan nähden.

    Kiittäen, 🙏

    **Linnea**, **Heidi**, **Mirva**, **Joni** ja **Andreas**
    """)

st.write("---")


st.header('📖 Käyttäjätarinoita: Tokmannin Tavoitteet 📖')
st.markdown("""
**Scrum käyttäjätarina**

Scrum-käyttäjätarina on lyhyt, yksinkertainen kuvaus ominaisuudesta tai toiminnosta, jota tuotteen loppukäyttäjä tarvitsee. Se on kirjoitettu käyttäjän näkökulmasta ja auttaa tiimiä ymmärtämään, mitä arvoa uusi ominaisuus tuo käyttäjälle. Käyttäjätarina koostuu yleensä kolmesta osasta: rooli, vaatimus ja liiketoimintaperuste.

**Asiakas/käyttäjä**

**Tilaaja Pekka Huttunen** on Tokmannin liiketoimintavastaava. Hän etsii uusia keinoja luoda hyödyllistä dataa asiakkaista ja analysoida Tokmannin tavaratalojen asiakaskäyttäytymistä ja liikehdintää. Tarkoitus on kerätä viikottaista ja vuosittaista dataa ja vahvistaa datavetoista liiketoimintaa.

Asiakkaalla oli esitiedoissa muutamia toiveita kuten: 

- **1. Kärryjen liikkeet kaupassa** 🛒
- **2. Kuumat alueet**¨🔥
- **3. Viikko-, kuukausi- ja vuosi-raportit** 📝
- **4. Läpimenoaikojen tilastointi** ⏱️
- **5. Kassojen aukioloajat** 📠
- **6. Kärryjen käyttöaste** 📈
- **7. Erilaisia hyödyllisiä tilastoja.** 📊

Kärrytilastointeja ja asiakaskäyttäytymistä käytetään jo olemassa olevan myynti/kassa-analysoinnin tukena, parantaakseen asiakaskokemusta ja myyntiä kivijalkamyymälöissä. Dataa halutaan hyödyntää myös sisäisesti myymälän vuoropäällikköjen suunnittelutyössä työn sujuvoittamisessa, kuten vuorosuunnitteluissa, hyllytyksien ja kuormien purkujen ajastamisessa ja asiakaspalvelun tehostamisessa.

**Asiakkaan tekninen asiantuntija Jaakko Vanhala** on asettanut datalle seuraavat vaatimukset: historiadataa pitäisi pystyä tilastoimaan ja analysoimaan, datapisteiden seuranta kaupan layoutissa, paikannustäsmällisyyden laatuvaatimus ja datan kohinan vähentäminen, x,y-koordinaattien skaalaus myymälän pohjakuvaan, visualisointi eri aikaväleillä ja viikonpäivinä, histogrammeja, useamman datalähteen yhdistäminen ja muuta asiakkaalle lisäarvoa tuottavaa.
""")

st.write("---")

st.write("**(live footage of us doing the project)**")
gif_link = "https://giphy.com/embed/ukMiDlCmdv2og"
st.markdown(f'<iframe src="{gif_link}" width="490" height="367" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
