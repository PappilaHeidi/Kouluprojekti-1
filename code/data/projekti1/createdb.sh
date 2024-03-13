#!/usr/bin/env bash
docker cp initdb.sql iiwari-mariadb-server:/var/lib/mysql/initdb.sql
docker exec -i iiwari-mariadb-server sh -c "/usr/bin/mariadb -u root --password=d41k4Duu < '/var/lib/mysql/initdb.sql'"