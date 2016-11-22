import sqlite3
import sqlcontroller as sql
import re
from __main__ import name

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
    results = sql.getIndexedTables(connection)
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

def printTables(indexedtables):
    for key, value in indexedtables.iteritems():
        print(key + " -- " + value)

def getSchemaInformation(connection, selectedname):
    name = regexTableName(selectedname)
    functionaldependencies = sql.getFunctionalDependencies(connection, name)
    properties = sql.getProperties(connection, name)
    print(properties)
    print(functionaldependencies)
    print(splitProperties(functionaldependencies[0]))
    return properties, functionaldependencies

def regexTableName(tablename):
    match = re.search("Input_(.*)", tablename)
    name = match.group(1)
    return name

# Splits the LHS and RHS of a functional dependency into separate characters.
# i.e) input: ['ABH','CK']
#      output: [['A', 'B', 'H'], ['C', 'K']]
def splitProperties(propertylist):
    return [list(propertylist[0]), list(propertylist[1])]
    
if  __name__ == "__main__":
    main()