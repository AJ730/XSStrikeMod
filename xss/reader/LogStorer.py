import sqlite3


class LogStorer:
    def __init__(self):
        self.conn = sqlite3.connect("vuln.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS vulnerability (
                    webpage TEXT,
                    type TEXT,
                    exploit TEXT,
                    succeeded TEXT,
                    no_change TEXT,
                    unknown_response TEXT,
                    blocked TEXT
            )""")
        self.conn.commit()
        self.conn.close()


    def addVector(self, createsPopup, url, paramName, vector, wholeUrl):
        conn = sqlite3.connect("vuln.db")
        c = conn.cursor()
        if createsPopup is None:
            createsPopup = False

        dict_vuln = (str(url), str(paramName), str(vector), str(createsPopup), "", "", "" )
        c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?, ?, ?)", dict_vuln)
        conn.commit()
        conn.close()







