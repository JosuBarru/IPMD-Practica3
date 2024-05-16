#!/usr/bin/env python3

import pyarrow.parquet as pq

parquet_file = "./Flights.parquet"

# Leer el esquema del archivo Parquet
table = pq.read_table(parquet_file)
schema = table.schema

print("Esquema del archivo Parquet:")
print(schema)

# Leer el contenido del archivo Parquet
data = table.to_pandas()

print("\nPrimeras filas del contenido del archivo Parquet:")
print(data.head())