import sqlite3
import re

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
    
    def insert(self, query, params = None):
        if (params is None):
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,params)
        self.conn.commit()
    
    def executemany(self, query, values):
        self.cursor.executemany(query,values)
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
    FDquery = """SELECT * FROM ?"""
    unparsed = connection.executeQuery(FDquery.replace("?", tablename))
    for item in unparsed:
        # append as [LHS,RHS] removing the delimiter.
        functionaldependencies.append( [str(item["LHS"].replace(',','')), str(item["RHS"].replace(',',''))] )
    return functionaldependencies

#Inputs: connection object, 
#        the dictionary in the form {'AB': [['A'], ['B']], 'AD': [], 'BC': [['B'], ['C']]}
#        name of the input table.
def createTables(connection, dictionary, name):
    # Get all attributes of the input table, and get their data type.
    inputtable = "Input_" + name
    olddatatypes = getDataTypes(connection, inputtable)
    
    for attributes, value in dictionary.iteritems():
        # Create the table names for the new output tables.
        valuetablename = "Output_" + name +"_"
        fdtablename =  "Output_FDs_" + name +"_"
        valuetablename += attributes
        fdtablename += attributes
        
        # Convert the attribute into a list i.e. "AB" -> ['A','B']
        key_as_list = list(attributes)
        # Drop the tables if the exist.
        dropquery = """DROP TABLE IF EXISTS {}""".format(valuetablename)
        connection.insert(dropquery)
        dropquery = """DROP TABLE IF EXISTS {}""".format(fdtablename)
        connection.insert(dropquery)
        
        # Create the relation table
        createquery = "CREATE TABLE {} (".format(valuetablename)
        for key in key_as_list:
            createquery += key + " " + olddatatypes[key]
            if (not key == key_as_list[len(key_as_list)-1]):
                createquery += ", "
        createquery += ");"
        connection.insert(createquery)
        
        # Insert the FDs into the table. Only if there is an FD.
        if (len(value) > 0):
            
            # Create the FD table
            createquery = "CREATE TABLE {} (LHS TEXT, RHS TEXT)".format(fdtablename)
            connection.insert(createquery)
        
            insertquery = """INSERT INTO {} VALUES (?,?)""".format(fdtablename)
            insertparams = (','.join(value[0][0]),','.join(value[0][1]))
            connection.insert(insertquery, insertparams)

#Inputs: connection object, 
#        the dictionary in the form {'AB': [['A'], ['B']], 'AD': [], 'BC': [['B'], ['C']]}
#        name of the input table.
def moveData(connection, dictionary, name):
    inputname = "Input_" + name
    for key in dictionary.keys():
        key_as_list = list(key)
        selectquery = """SELECT """ + ','.join(key_as_list) + " FROM {}".format(inputname)
        results = connection.executeQuery(selectquery)
        outputtable = "Output_" + name + "_" + key
        insertquery = """INSERT INTO {} VALUES (""".format(outputtable)
        for i in range(0, len(key_as_list)):
            insertquery += "?"
            if (not i == len(key_as_list)-1):
                insertquery += ","
        insertquery += ")"
        connection.executemany(insertquery, results)
    
def getDataTypes(connection, tablename):
    output = {}
    query = """PRAGMA table_info({})""".format(tablename)
    result = connection.executeQuery(query)
    for item in result:
        output[item["name"]] = item["type"]
    return output

if __name__ == "__main__":
    ## UNIT TESTING
    connection = connectDatabase("MiniProject2-InputOutputExample3NF.db")
    dictlol = {'AB': [['A'], ['B']], 'AD': [], 'BC': [['B'], ['C']]}
    moveData(connection, dictlol, "R5")