import sqlcontroller as sql
import re
import helper
import bcnf
import threenf

def main():
    databasepath = raw_input("Enter the database name: ")
    print("")
    if(databasepath == ""):
        databasepath = "MiniProject2-InputExample.db"
    connection = sql.connectDatabase(databasepath);
    
    while True:
        print("1. Read input schema.")
        print("2. Compute attribute closure of a set of attributes")
        print("3. Determine whether two sets of functional dependencies are equivalent.")
        print("4. Quit")
        selectedindex = raw_input("What do you want to do? : ")
        print("")
        if (selectedindex == '1'):
            readInputSchema(connection)
        elif (selectedindex == '2'):
            helper.functionality_one(connection)
        elif (selectedindex == "3"):
            helper.functionality_two(connection)
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
    selectedindex = raw_input("Select a schema you want to use as an input [or press 'b' to go back]: ")
    print("")
    if (selectedindex.lower() == "b"):
        return;
    elif (selectedindex not in results.keys()):
        print("Schema not found. Please input correct index.")
    else:
        selectedname = results[selectedindex] 
        attributes, functionaldependencies, name = getSchemaInformation(connection, selectedname)
        printInformation(attributes, functionaldependencies)
        
        while True:
            print("1. Synthesize 3NF schema.")
            print("2. Decompose the input table into BCNF.")
            print("3. Select a different input schema.")
            
            selectedindex = raw_input("What do you want to do? : ")
            print("")
            if (selectedindex == '1'):
                threenf.threenfInterface(connection, attributes, functionaldependencies, name)
                return;
            elif (selectedindex == '2'):
                bcnf.BCNFInterface(connection, attributes, functionaldependencies, name )
                return;
            elif (selectedindex == '3'):
                readInputSchema(connection);
                return;

def printInformation(attributes, functionaldependencies):
    print("The selected schema has the following information: \n")
    print("Attributes: " + ', '.join(attributes))
    fdstring = ""
    for fd in functionaldependencies:
        fdstring += fd[0] + " --> " + fd[1]
        if (fd is not functionaldependencies[len(functionaldependencies)-1]):
            fdstring += ", "
    print("Functional dependencies: " + fdstring)
    print("")
    
def printTables(indexedtables):
    for key, value in indexedtables.iteritems():
        print(key + " -- " + value)

def getSchemaInformation(connection, selectedname):
    name = regexTableName(selectedname)
    functionaldependencies = sql.getFunctionalDependencies(connection, "Input_FDs_" + name)
    attributes = sql.getAttributes(connection, name)
    return attributes, functionaldependencies, name

def regexTableName(tablename):
    match = re.search("(?:Input_|Output_)(.*)", tablename)
    name = match.group(1)
    return name

# Splits the LHS and RHS of a functional dependency into separate characters.
# i.e) input: ['ABH','CK']
#      output: [['A', 'B', 'H'], ['C', 'K']]
def splitProperties(propertylist):
    return [list(propertylist[0]), list(propertylist[1])]
    
if  __name__ == "__main__":
    main()