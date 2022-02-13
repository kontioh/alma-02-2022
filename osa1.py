import json
import csv


## Parse data from json to CSV ##
def parseData(srcPath, dstPath):
  # Read the json file
  f = open(srcPath)
  jsonData = json.load(f)
  f.close()

  # Store columns and data into lists
  columns = jsonData.get("columns")
  data = jsonData.get("data")

  # Open the destination csv
  f = csv.writer(open(dstPath, "w"))
  
  # Write headers
  f.writerow(columns)

  # Write the data
  for d in data:
    f.writerow(d["keys"] + d["values"])


# Call the function to parse the json data
parseData("./data/ansiotasoindeksi.json", "parsed-files/ansiotasoindeksi.csv")
parseData("./data/uusien_osakeasuntojen_hintaindeksi.json", "parsed-files/uusien_osakeasuntojen_hintaindeksi.csv")
parseData("./data/vuokraindeksi.json", "parsed-files/vuokraindeksi.csv")
