import sqlite3


class LogStorer:
    def __init__(self):
        self.conn = sqlite3.connect("vuln.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS vulnerability (
                    webpage TEXT,
                    type TEXT,
                    exploit TEXT,
                    status TEXT,
                    WAF
            )""")
        self.conn.commit()
        self.conn.close()


    def addVector(self, createsPopup, url, paramName, vector, wholeUrl, WAF):
        conn = sqlite3.connect("vuln.db")
        c = conn.cursor()

        dict_vuln = (str(url), str(paramName), str(vector), str(createsPopup), str(WAF))
        c.execute("INSERT INTO vulnerability VALUES (?, ?, ?, ?, ?)", dict_vuln)
        conn.commit()
        conn.close()

    def getColumn(self, is_row):
        conn = sqlite3.connect("vuln.db")
        c = conn.cursor()
        c.execute(f"SELECT rowid FROM vulnerability WHERE webpage LIKE '%{is_row}%'")
        data = c.fetchall()

        conn.commit()
        conn.close()

        if len(data) == 0:
            return False
        return True






