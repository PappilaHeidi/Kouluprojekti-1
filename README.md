# Dockerfile
Rakenna docker image

Siirry oikeaan hakemistoon
```shell=
cd /code/jupyter_workshop
```

rakenna levykuva
```shell=
docker build -t jupyter-workshop . #dockerfile on /code/jupyter_workshop kansiossa

# Ympäristön pystyttäminen

Aja projektin juurikansiossa komento

```shell=
docker-compose up
```

Jos lisäät kirjastoja jupyter ympäristöön (requirements.txt), niin rakenna levykuva uusiksi


# Ympäristön alasajo

Aja projektin juurikansiossa komento

```shell=
docker-compose down
```

tai ctrl+c

# Jupyterlab

Avaa jupyter-ympäristö selaimessa http://localhost:8889 ja loihdi tokeniin `daika`. Tämän myötä sinulle pitäisi avautua projektin touhuympäristö. Avaa siinä ympäristössä tiedosto `start.ipynb` ja suorita kaikki koodisolut ylhäältä alas. Loppuun pitäisi piirtyä kartta, jossa on punaisia pisteitä.

# Yhteys tietokantaan

```shell=
# Yhteys tietokantakonttiin
docker exec -it iiwari-mariadb-server bash

# Yhteys tietokantaan
/usr/bin/mariadb -u root --password=d41k4Duu

# SELECT
USE iiwari_org;

SELECT COUNT(*) FROM SensorData;
```