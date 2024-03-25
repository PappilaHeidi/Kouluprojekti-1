#!/usr/bin/env bash
docker cp initdb.sql iiwari-mariadb-server:/var/lib/mysql/initdb.sql
docker exec -i iiwari-mariadb-server sh -c "/usr/bin/mariadb -u root --password=d41k4Duu < '/var/lib/mysql/initdb.sql'" 
#1. suorittaa iiwari-mariadb kontissa seuraavat asiat: 1. mariadb sovellus ajetaan -u root käyttäjällä +salasana, johon syötetään < (input) 
#ylemmällä rivillä kopioitu initdb tiedosto. Tämä luo ensimmäisen taulun tietokantaan