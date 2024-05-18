# Projektiopinnot 1: Datan hallinta (2024) - Keskivahavat-suorittajat
Jäsenet:
Andreas Konga

Joni Kauppinen

Linnea Pekkanen

Mirva Kirvesniemi

Heidi Pappila

# Projektin kuvaus
Tässä projektissa pyritään asiakkaalle, eli Tokmannille, tarjoamaan syvällistä ja hyödyllistä analyysiä toimitetusta datasta, joka perustuu asiakkaiden kärryihin ja niiden liikkeisiin Tokmannin pohjapiirroksessa. Vaikka emme tiedä tarkalleen, miltä hyllyltä löytyy mitäkin tuotetta, voimme silti analysoida asiakkaiden liikkumismalleja myymälässä. Tavoitteena on ymmärtää, miten asiakkaat navigoivat myymälässä, tunnistaa suosituimmat reitit ja alueet, sekä havaita mahdolliset pullonkaulat ja tehottomat alueet.

Tämän analyysin avulla voimme tarjota Tokmannille tietoa siitä, miten myymälän layout vaikuttaa asiakkaiden ostokäyttäytymiseen. Voimme esimerkiksi tunnistaa alueet, joissa asiakkaat viettävät eniten aikaa tai reitit, joita pitkin asiakkaat yleensä liikkuvat. Tämä voi auttaa optimoimaan myymälän layoutia ja parantamaan asiakaskokemusta, vaikka emme tiedä tarkalleen tuotteiden sijainteja.

# Asennus- ja käyttöohjeet

*Kaikki vaaditut riippuvuudet asentuvat docker-compose build -komennon yhteydessä.*

## Dockerfile ja Docker-compose pystytys terminaalissa

**Rakenna levykuvat ja kontit**
```shell=
docker-compose build
```

**Docker-konttien käynnistys**
```shell=
docker-compose up
```

**Ympäristön alasajo**
```shell=
ctrl + c 
tai
docker-compose down
```

## Virtualenv asentaminen terminaalissa

Asenna virtualenv komennolla:
```pip install virtualenv```

```python -m venv .venv```

Aktivoi .venv:
```.venv/Scripts/activate```

Asenna paketit:
```pip install -r requirements.txt```

## Jupyterlab
Avaa jupyter-ympäristö selaimessa http://localhost:8889 ja kirjoita token.

Token: 
```daika```

## Streamlit
Avaa selaimessa http://localhost:8501.

# DuckDB:n alustaminen & Tietokanta arkkitehtuuri & ETL

Tässä projektissa tullaan noudattamaan löyhästi Medallion Architecturen mukaista tietokanta arkkitehtuuria, jossa tietokantataulut voidaan jakaa kolmeen kategoriaan, Bronze, Silver ja Gold. Medallion architecture on yksinkertainen ja selkeä tapa hallinnoida datan tallentamista. Kyseisen arkkitehtuurin ansiosta, data ja sen muutokset pysyvät läpinäkyvinä ja helposti dokumentoitavissa läpi kaikkien eri prosessien vaiheiden.

Bronze-taso, eli "bronze_"- prefixillä tallennetut tietokanta taulut kuvaavat dataa, johon tallennetaan pelkästään raakadataa lähtöjärjestelmistä. Tämän projektin kontekstissa sinne tullaan tallentamaan kaikkien CSV-tiedostojen data

Silver-taso eli "silver_" -prefixillä tallennetut tietokanta taulut tulee pitämään putsattua ja esikäsiteltyä dataa bronze-tasolta. Tähän dataan on voitu tehdä putsauksia, suodatuksia, että data olisi helppokäyttöisemmässä muodossa. Silver-tason muutokset ovat hyvin kevyitä ja datoja voidaan tällä tasolla yhdistellä.

Gold-taso eli "gold_" -prefixillä tallennetut tietokanta taulut pitävät sisällään lopullisen datan ja sen pohjalta voidaan tehdä erilaisia analyysejä tai hyödyntää sellaiseenan vaikka raporteissa. 

Puretaan kaikki CSV-tiedostot code/data/files -pathiin.
Kopioinnin jälkeen avaa code/bronze_pipeline.ipynb notebook
Kyseinen notebook hoitaa Bronze-tason ETL-putken prosessoinnin, eli siirtää kaikki code/data/files -pathiin tallennetut CSV-tiedostot tietokantatauluun
Kyseisen notebookin ajamalla saat itsellesi lokaalisti luotua DuckDB tietokannan ja sinne kaikki raakadatan, jota voi hyödyntää tässä projektissa.
Tämän jälkeen ajetaan code/silver_pipeline.ipynb notebook, jossa tehdään yksinkertaiset datan esikäsittelyt ja prosessoinnit

Muista aina DuckDB yhteyden lopussa käyttää "conn.close()", jotta Tietokanta yhteys tulee suljettua, useita yhteyksiä ei voi olla päällekkäin käytössä.