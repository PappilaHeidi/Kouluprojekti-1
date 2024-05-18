# Projektiopinnot 1: Datan hallinta (2024) - Keskivahavat-suorittajat
Tekijät:

- Andreas Konga
- Joni Kauppinen
- Linnea Pekkanen
- Mirva Kirvesniemi
- Heidi Pappila

# Projektin kuvaus
Tässä projektissa pyritään asiakkaalle, eli Tokmannille, tarjoamaan syvällistä ja hyödyllistä analyysiä toimitetusta datasta, joka perustuu asiakkaiden kärryihin ja niiden liikkeisiin Tokmannin pohjapiirroksessa. Vaikka emme tiedä tarkalleen, miltä hyllyltä löytyy mitäkin tuotetta, voimme silti analysoida asiakkaiden liikkumismalleja myymälässä. Tavoitteena on ymmärtää, miten asiakkaat navigoivat myymälässä, tunnistaa suosituimmat reitit ja alueet, sekä havaita mahdolliset pullonkaulat ja tehottomat alueet.

Tämän analyysin avulla voimme tarjota Tokmannille tietoa siitä, miten myymälän layout vaikuttaa asiakkaiden ostokäyttäytymiseen. Voimme esimerkiksi tunnistaa alueet, joissa asiakkaat viettävät eniten aikaa tai reitit, joita pitkin asiakkaat yleensä liikkuvat. Tämä voi auttaa optimoimaan myymälän layoutia ja parantamaan asiakaskokemusta, vaikka emme tiedä tarkalleen tuotteiden sijainteja.

# Asennus- ja käyttöohjeet

*Kaikki vaaditut riippuvuudet asentuvat docker-compose build -komennon yhteydessä.*

## Dockerfile ja Docker-compose pystytys terminaalissa

1. **Rakenna levykuvat ja kontit:**
```shell=
docker-compose build
```

2. **Docker-konttien käynnistys:**
```shell=
docker-compose up
```

3. **Ympäristön alasajo:**
```shell=
ctrl + c 
tai
docker-compose down
```

## Virtualenv asentaminen terminaalissa

1. **Asenna virtualenv komennolla:**
```pip install virtualenv```

2. **Luo uusi virtuaaliympäristö komennolla:**
```python -m venv .venv```

3. **Aktivoi .venv:**
```.venv/Scripts/activate```

4. **Asenna paketit:**
```pip install -r requirements.txt```

## Jupyterlab
Avaa jupyter-ympäristö selaimessa http://localhost:8889 ja kirjoita token.

Token: 
```daika```

## Streamlit
Avaa selaimessa http://localhost:8501.

# DuckDB:n alustaminen & Tietokanta arkkitehtuuri & ETL

Tässä projektissa tullaan noudattamaan löyhästi Medallion Architecturen mukaista tietokanta arkkitehtuuria, jossa tietokantataulut voidaan jakaa kolmeen kategoriaan: Bronze, Silver ja Gold. Medallion architecture on yksinkertainen ja selkeä tapa hallinnoida datan tallentamista. Kyseisen arkkitehtuurin ansiosta, data ja sen muutokset pysyvät läpinäkyvinä ja helposti dokumentoitavissa läpi kaikkien eri prosessien vaiheiden.

- ```Bronze-taso```, eli "bronze_"- prefixillä tallennetut tietokanta taulut kuvaavat dataa, johon tallennetaan pelkästään raakadataa lähtöjärjestelmistä. Tämän projektin kontekstissa sinne tullaan tallentamaan kaikkien CSV-tiedostojen data

- ```Silver-taso```, eli "silver_" -prefixillä tallennetut tietokanta taulut tulee pitämään putsattua ja esikäsiteltyä dataa bronze-tasolta. Tähän dataan on voitu tehdä putsauksia, suodatuksia, että data olisi helppokäyttöisemmässä muodossa. Silver-tason muutokset ovat hyvin kevyitä ja datoja voidaan tällä tasolla yhdistellä.

- ```Gold-taso eli```, "gold_" -prefixillä tallennetut tietokanta taulut pitävät sisällään lopullisen datan ja sen pohjalta voidaan tehdä erilaisia analyysejä tai hyödyntää sellaiseenan vaikka raporteissa. 

**ETL-prosessi**

1. **CSV-tiedostojen purkaminen:**
- Puretaan kaikki CSV-tiedostot ```code/data/files``` -hakemistoon.

2. **Bronze-tason ETL-putki:**
- Aja ```code/bronze_pipeline.ipynb``` -notebook
- Tämä notebook prosessoi kaikki ```code/data/files``` -hakemistoon tallennetut CSV-tiedostot tietokantatauluun.
- Notebookin ajamisen jälkeen DuckDB-tietokanta sisältää raakadatan, jota voi hyödyntää projektissa.

3. **Silver-tason ETL-putki:**
- Aja ```code/silver_pipeline.ipynb``` -notebook, jossa tehdään datan esikäsittelyt ja prosessoinnit.

4. **Gold-tason ETL-putki:**
- Aja ```code/gold_pipeline.ipynb``` -notebook.
- Tässä notebookissa yhdistellään ja aggregoidaan silver-tason taulut lopullisiin gold-tason tauluihin.
- Lopullinen data sisältää analyysejä ja raportteja varten tarvittavat tiedot.

**Huomio:**
Muista aina DuckDB yhteyden lopussa käyttää ```conn.close()```, jotta Tietokanta yhteys tulee suljettua. Sillä useita yhteyksiä ei voi olla päällekkäin käytössä.