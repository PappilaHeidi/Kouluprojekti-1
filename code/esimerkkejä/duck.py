""" Tässä kelpo esimerkki DuckDB:n suorituskyvystä vs. any-other-database
"""

import time
import duckdb

start = time.time()

data = duckdb.sql("SELECT * FROM './data/projekti1/*.csv' WHERE timestamp \
                   BETWEEN '2019-04-01 00:00:00' AND '2019-04-30 00:00:00'" )

print(data)

mid = time.time()

data.to_csv("./data/tulos.csv")

end = time.time()

print(f"Read/Parse: {mid-start}")
print(f"CSV-output: {end-mid}")