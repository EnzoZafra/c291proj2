import sqlite3
import sqlcontroller as sql
import re

def main():
    databasepath = raw_input("Enter the database name: ")
    if(databasepath == ""):
        databasepath = "MiniProject2-InputExample.db"
    connection = sql.connectDatabase(databasepath);
    
    while True:
        print("1. Read input schema.")
        print("2. Compute attribute closure of a set of attributes")
        print("3. Determine whether two sets of functional dependencies are equivalent.")
        print("4. Quit")
        selectedindex = raw_input("What do you want to do? : ")
        if (selectedindex == '1'):
            readInputSchema(connection)
        elif (selectedindex == '2'):
            # TODO:
            print("NOT IMPLEMENTED")
        elif (selectedindex == "3"):
            # TODO:
            print("Not IMPLEMENTED")
        elif (selectedindex == "4"):
            print("Goodbye...")
            break;
        else:
            print("Can't find correct action. Please select another.")
            print("1. Read input schema.")
            print("2. Compute attribute closure of a set of attributes")
            print("3. Determine whether two sets of functional dependencies are equivalent.")
            print("4. Quit")

def readInputSchema(connection):
    results = getIndexedTables(connection)
    printTables(results)
    selectedindex = raw_input("Select a schema you want to use as an input [or press 'q' to quit]: ")
    if (selectedindex not in results.keys()):
        print("Schema not found. Please input correct index.")
    else:
        selectedname = results[selectedindex] 
        properties, functionaldependencies = getSchemaInformation(connection, selectedname)
        
        while True:
            print("1. Synthesize 3NF schema.")
            print("2. Decompose the input table into BCNF.")
            print("3. Select a different input schema.")
            
            selectedindex = raw_input("What do you want to do? : ")
            if (selectedindex == '1'):
                # TODO:
                print("Not implemented")
            elif (selectedindex == '2'):
                # TODO:
                print("Not implemented")
            elif (selectedindex == '3'):
                return;
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