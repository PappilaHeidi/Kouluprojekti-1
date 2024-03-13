""" Tässä kelpo esimerkki DuckDB:n suorituskyvystä vs. any-other-database
"""
import duckdb

data = duckdb.sql("SELECT COUNT(*) FROM './data/projekti1/*.csv' WHERE timestamp BETWEEN '2019-04-01 00:00:00' AND '2019-04-31 04:25:00'" )
#data = duckdb.sql("SELECT COUNT(*) FROM './data/projekti1/*.csv'" )

print(data)