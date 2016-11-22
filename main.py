import sqlite3
import sqlcontroller as sql
import re

def main():
    databasepath = raw_input("Enter the database name: ")
    if(databasepath == ""):
        databasepath = "MiniProject2-InputExample.db"
    connection = sql.connectDatabase(databasepath);
    results = getIndexedTables(connection)
    
    printTables(results)
    while True:
        selectedindex = raw_input("Select a schema you want to use as an input [or press 'q' to quit]: ")
        if (selectedindex == 'q'):
            break;
        elif (selectedindex not in results.keys()):
            print("Schema not found. Please input correct index.")
        else:
            selectedname = results[selectedindex] 
            properties, functionaldependencies = getSchemaInformation(connection, selectedname)
            
            while True:
                print("1. Read input schema.")
                print("2. Synthesize 3NF schema")
                print("3. Decompose table into BCNF")
                print("4. Compute attribute closure of a set of attributes")

def getIndexedTables(connection):
    query = """SELECT name, sql FROM SQLITE_MASTER WHERE name LIKE 'INPUT_%' AND name NOT LIKE 'INPUT_FD%';"""
    results = connection.executeQuery(query)
    indexedresults = {}
    for i in range(0,len(results)):
        indexedresults[str(i+1)] = results[i]["name"]
    return indexedresults;

def printTables(indexedtables):
    for key, value in indexedtables.iteritems():
        print(key + " -- " + value)

def getSchemaInformation(connection, selectedname):
    match = re.search("Input_(.*)", selectedname)
    name = match.group(1)
    functionaldependencies = getFunctionalDependencies(connection, name)
    properties = getProperties(connection, name)
    print(properties)
    print(functionaldependencies)
    print(splitProperties(functionaldependencies[0]))
    return properties, functionaldependencies
    
def getValues(connection, tablename):
    name = "Input_" + tablename 
    FDquery = """SELECT * FROM ?"""
    values = connection.executeQuery(FDquery.replace("?", name))
    return values

def getProperties(connection, tablename):
    name = "Input_" + tablename 
    FDquery = """SELECT * FROM ?"""
    values = connection.getkeys(FDquery.replace("?", name))
    return values

def getFunctionalDependencies(connection, tablename):
    functionaldependencies = []
    name = "Input_FDs_" + tablename 
    FDquery = """SELECT * FROM ?"""
    unparsed = connection.executeQuery(FDquery.replace("?", name))
    for item in unparsed:
        # append as [LHS,RHS] removing the delimiter.
        functionaldependencies.append( [str(item["LHS"].replace(',','')), str(item["RHS"].replace(',',''))] )
    return functionaldependencies

# Splits the LHS and RHS of a functional dependency into separate characters.
# i.e) input: ['ABH','CK']
#      output: [['A', 'B', 'H'], ['C', 'K']]
def splitProperties(propertylist):
    return [list(propertylist[0]), list(propertylist[1])]
    
if  __name__ == "__main__":
    main()