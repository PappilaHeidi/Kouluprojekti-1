# Dockerfile
Pystytä docker ensimmäistä kertaa

rakenna levykuvat ja kontit terminaalissa
```shell=
docker-compose build

# Ympäristön pystyttäminen

Docker-konttien käynnistys
```shell=
docker-compose up
```

# Virtualenv asentaminen

Asenna virtualenv komennolla

```pip install virtualenv```

```python -m venv .venv```

Aktivoi .venv
```.venv/Scripts/activate```

Asenna paketit

```pip install -r requirements.txt```

# Ympäristön alasajo

Aja projektin juurikansiossa komento

```shell=
docker-compose down
```

tai ctrl+c

# Jupyterlab

Avaa jupyter-ympäristö selaimessa http://localhost:8889 ja loihdi tokeniin `daika`. Tämän myötä sinulle pitäisi avautua projektin touhuympäristö. Avaa siinä ympäristössä tiedosto `start.ipynb` ja suorita kaikki koodisolut ylhäältä alas. Loppuun pitäisi piirtyä kartta, jossa on punaisia pisteitä.

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