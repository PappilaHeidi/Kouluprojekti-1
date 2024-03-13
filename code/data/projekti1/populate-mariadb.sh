#!/usr/bin/env bash
for f in "${PWD}"/*.csv
do
   echo Working on $f
   docker cp "$f" iiwari-mariadb-server:/tmp/SensorData.csv
   docker exec -i iiwari-mariadb-server sh -c "/usr/bin/mariadb-import --ignore-lines='1' --fields-terminated-by=',' --user=root --password=d41k4Duu iiwari_org /tmp/SensorData.csv"
   docker exec -i iiwari-mariadb-server sh -c "rm /tmp/SensorData.csv"
done