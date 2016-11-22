import sqlite3

class sqlcontroller:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
    
    def executeQuery(self, query, params = None):
        if (params is None):
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,params)
        results = self.cursor.fetchall()
        return results
    
    def getkeys(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchone()
        return results.keys()
    
    def insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

# Connects to the database
def connectDatabase(filelocation):
    conn = sqlite3.connect(filelocation)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return sqlcontroller(conn,c)