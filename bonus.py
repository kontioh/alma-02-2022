import json
import pandas as pd


def jsonToDataFrame(filePath):
  # Read json
  f = open(filePath)
  jsonData = json.load(f)
  f.close()

  # Extract column names and data
  df_columns = pd.json_normalize(jsonData, record_path="columns")
  df_data = pd.json_normalize(jsonData, record_path="data")

  # Create a new DataFrame with flattened data ("keys" and "values")
  df = pd.DataFrame(columns=df_columns[0], data=(df_data["keys"] + df_data["values"]).to_list())

  return df


# Read json contents to corresponding DataFrames 
# (could also be read from the parsed CSV files with command 'pd.read_csv("parsed-files/vuokraindeksi.csv")')
df_vuokraindeksi = jsonToDataFrame("data/vuokraindeksi.json")
df_uusien_osakeasuntojen_hintaindeksi = jsonToDataFrame("data/uusien_osakeasuntojen_hintaindeksi.json")

df_v = df_vuokraindeksi[["Vuosineljannes", "Alue", "Huoneluku", "Indeksi", "Vuokra_per_nelio"]].rename({"Indeksi": "Vuokraindeksi"}, axis="columns")
df_u = df_uusien_osakeasuntojen_hintaindeksi[["Vuosineljannes", "Alue", "Huoneluku", "Kauppojen lukumäärä"]]

# Merge df_v and dv_u
df_vu = pd.merge(df_v, df_u, on=["Vuosineljannes", "Alue", "Huoneluku"])


# Group by "Alue" & "Huoneluku"
df_grouped = df_vu.groupby(by=["Alue", "Huoneluku"], sort=False).agg(
  Kauppojen_määrän_maksimi = ("Kauppojen lukumäärä", "max"),
  Kauppojen_määrä_yhteensä = ("Kauppojen lukumäärä", "sum"),
  Vuokraindeksin_keskiarvo = ("Vuokraindeksi", "mean"),
  Vuokra_per_nelio_maksimi = ("Vuokra_per_nelio", "max")
  )
df_grouped.reset_index(inplace=True)


# Print the final dataframe
print(df_grouped)
