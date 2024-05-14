import pandas as pd

# Cargar el archivo Parquet
flights_df = pd.read_parquet("Flights.parquet")

# Guardar como archivo JSON
flights_df.to_json("Flights.json", orient="records")

