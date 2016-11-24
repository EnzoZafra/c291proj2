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

def getIndexedTables(connection):
    query = """SELECT name, sql FROM SQLITE_MASTER WHERE name LIKE 'INPUT_%' AND name NOT LIKE 'INPUT_FD%';"""
    results = connection.executeQuery(query)
    indexedresults = {}
    for i in range(0,len(results)):
        indexedresults[str(i+1)] = results[i]["name"]
    return indexedresults;

def getValues(connection, tablename):
    name = "Input_" + tablename 
    FDquery = """SELECT * FROM ?"""
    values = connection.executeQuery(FDquery.replace("?", name))
    return values

def getAttributes(connection, tablename):
    name = "Input_" + tablename 
    FDquery = """SELECT * FROM ?"""
    values = connection.getkeys(FDquery.replace("?", name))
    return values

# Returns the functional dependencies from a table in the form [ [LHS1, RHS1] , [LHS2, RHS2] , [LHS3, RHS3] ]
def getFunctionalDependencies(connection, tablename):
    functionaldependencies = []
    name = "Input_" + tablename 
    FDquery = """SELECT * FROM ?"""
    unparsed = connection.executeQuery(FDquery.replace("?", name))
    for item in unparsed:
        # append as [LHS,RHS] removing the delimiter.
        functionaldependencies.append( [str(item["LHS"].replace(',','')), str(item["RHS"].replace(',',''))] )
    return functionaldependencies