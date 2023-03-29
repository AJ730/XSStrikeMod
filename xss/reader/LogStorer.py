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


    def addVector(self, createsPopup, url, paramName, vector, wholeUrl):
        dict_vuln = (url, paramName, vector, str(createsPopup), "", "", "" )
        self.c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?, ?, ?)", dict_vuln)








