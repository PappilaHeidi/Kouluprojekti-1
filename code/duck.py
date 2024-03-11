""" Tässä kelpo esimerkki DuckDB:n suorituskyvystä vs. any-other-database
"""
import duckdb

data = duckdb.sql("SELECT * FROM './data/node3200.kevennetty.csv' WHERE timestamp BETWEEN '2019-04-06 00:00:00' AND '2019-04-06 04:25:00'" )
print(data)