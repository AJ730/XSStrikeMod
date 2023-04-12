import sqlite3

conn1 = sqlite3.connect("vuln1.db")
conn2 = sqlite3.connect("vuln2.db")
conn3 = sqlite3.connect("vuln3.db")
conn4 = sqlite3.connect("vuln4.db")
conn = sqlite3.connect("output.db")

c1 = conn1.cursor()
c2 = conn2.cursor()
c3 = conn3.cursor()
c4 = conn4.cursor()
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS vulnerability (
                    webpage TEXT,
                    type TEXT,
                    exploit TEXT,
                    status TEXT,
                    WAF
            )""")

c1.execute("SELECT * FROM vulnerability")
c2.execute("SELECT * FROM vulnerability")
c3.execute("SELECT * FROM vulnerability")
c4.execute("SELECT * FROM vulnerability")

rows1 = c1.fetchall()
rows2 = c2.fetchall()
rows3 = c3.fetchall()
rows4 = c4.fetchall()

for row in rows1:
    dict_vuln = (row[0], row[1], row[2], row[3], row[4])
    c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?)", dict_vuln)

for row in rows2:
    dict_vuln = (row[0], row[1], row[2], row[3], row[4])
    c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?)", dict_vuln)

for row in rows3:
    dict_vuln = (row[0], row[1], row[2], row[3], row[4])
    c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?)", dict_vuln)

for row in rows4:
    dict_vuln = (row[0], row[1], row[2], row[3], row[4])
    c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?)", dict_vuln)


print("It does not commit the changes currently because I manually disabled it, because otherwise we would have duplicates")
#conn.commit()
#conn.close()