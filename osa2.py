import sqlite3

from matplotlib.cbook import flatten

con = sqlite3.connect("./data/database.db")
cur = con.cursor()


# Delete duplicate rows from the table ansiotasoindeksi 
# (was only run once for the initial data; no need to run again)

#cur.execute('''DELETE FROM ansiotasoindeksi 
#  WHERE rowid NOT IN (
#    SELECT MIN(rowid)
#    FROM ansiotasoindeksi
#    GROUP BY Vuosineljannes, Ansiotasoindeksi
#    )''')
#con.commit()



################################################
## 3. Ansioindeksin ja hintaindeksin vertailu ##
################################################

# Jokaista vuosineljännestä ja huonelukua vastaavat ansioindeksit,
# hintaindeksit ja vuokraindeksit Helsingin alueelta:

res = cur.execute('''
  SELECT DISTINCT
    u.Vuosineljannes,
    u.Alue,
    u.Huoneluku,
    ansiotasoindeksi AS Ans_indeksi,
    u.Indeksi AS Hintaindeksi,
    v.Indeksi AS Vuokraindeksi
  FROM 
    uusien_osakeasuntojen_hintaindeksi AS u
  INNER JOIN ansiotasoindeksi AS a 
    ON u.Vuosineljannes = a.Vuosineljannes
  INNER JOIN vuokraindeksi AS v
    ON u.Vuosineljannes = v.Vuosineljannes AND u.Huoneluku = v.Huoneluku
  WHERE u.Alue = "Helsinki" AND v.Alue = "Helsinki"
  ''')

result3 = [tuple([i[0] for i in cur.description])]
for row in res:
  result3.append(row)



###############################################################
## 4. Yksiöiden yhteislukumäärä kaikilta vuosineljänneksiltä ##
###############################################################

# Summa myydyistä yksiöiden lukumääristä kaikilta vuosineljänneksiltä
# Helsingin ja Espoo-Kauniainen alueelta:

res = cur.execute('''
  SELECT Vuosineljannes, SUM(`Kauppojen lukumäärä`) AS `Kauppojen lkm (yksiöt)`
  FROM 
    uusien_osakeasuntojen_hintaindeksi
  WHERE 
    Huoneluku = "Yksiot"
    AND (Alue = "Helsinki" OR Alue = "Espoo-Kauniainen")
  GROUP BY Vuosineljannes
  ''')

result4 = [tuple([i[0] for i in cur.description])]
for row in res:
  result4.append(row)



######################################################
## 5. Vuokra- ja hintaindeksin suhde ansioindeksiin ##
######################################################

# Vuokra-ansioindeksi ja hinta-ansioindeksi Vantaan alueelta 
# kaikilta vuosineljänneksiltä:

res = cur.execute('''
  SELECT
    u.Vuosineljannes,
    u.Alue,
    u.Huoneluku,
    ROUND(ansiotasoindeksi / v.Indeksi, 2) AS `Vuokra-ansioindeksi`,
    ROUND(ansiotasoindeksi / u.Indeksi, 2) AS `Hinta-ansioindeksi`
  FROM 
    uusien_osakeasuntojen_hintaindeksi AS u
  INNER JOIN ansiotasoindeksi AS a 
    ON u.Vuosineljannes = a.Vuosineljannes
  INNER JOIN vuokraindeksi AS v
    ON u.Vuosineljannes = v.Vuosineljannes AND u.Huoneluku = v.Huoneluku
  WHERE u.Alue = "Vantaa" AND v.Alue = "Vantaa"
  ''')

result5 = [tuple([i[0] for i in cur.description])]
for row in res:
  result5.append(row)


# Close the database connection
con.close()


#######################
## Print the results ##
#######################

print("3. Ansioindeksin ja hintaindeksin vertailu")
for r in result3:
  print(r)

print("\n4. Yksiöiden yhteislukumäärä kaikilta vuosineljänneksiltä")
for r in result4:
  print(r)

print("\n5. Vuokra- ja hintaindeksin suhde ansioindeksiin")
for r in result5:
  print(r)