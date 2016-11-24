import main
import sqlcontroller as controller

# attribute_list in the form of : ['A','B']
# combined_fds in the form of : [ [['A','B'], ['C']], [['C'],['D']] ]
#                                    (AB -> C)            (C -> D)
# If your inputs are above, this should return ['A','B','C','D']
def computeClosure(attribute_list, combined_fds):
    closure = attribute_list
    old = []
    while (old != closure):
        old = closure
        for fd in combined_fds:
            LHS = fd[0] 
            RHS = fd[1]
            if set(LHS).issubset(closure) and not set(RHS).issubset(closure):
                closure = list(set(closure).union(RHS))
    return closure;
            
def getMultipleFDs(connection, list_names):
    combinedFDs = []
    for name in list_names:
        fd = controller.getFunctionalDependencies(connection, main.regexTableName(name))
        for item in fd:
            combinedFDs.append(main.splitProperties(item))
    return combinedFDs

# Checks if two lists of functional dependencies are equal.
def checkEqual(fd1, fd2):
    for fd in fd1:
        print(fd)
        if (not fdTest(fd, fd2)):
            return False
    for fd in fd2:
        if (not fdTest(fd, fd1)):
            return False
    return True

def fdTest(memberCandidate, list_of_fds):
    lhsClosure = computeClosure(memberCandidate[0],
            list_of_fds);
    return set(memberCandidate[1]).issubset(lhsClosure)
    
def functionality_one(connection):
    attribute_input = raw_input("Please enter the list of attributes [i.e = 'A,B,C']: ").upper()
    attribute_list = attribute_input.replace(' ','').split(',')
    if (not checkAllAttributesSingle(attribute_list)):
        print("There is an error with the list of attributes you input.")
        return
    
    tablenames_input = raw_input("Please enter the list of table names to get the functional dependencies from: ")
    print("")
    tablenames_list = tablenames_input.replace(' ', '').split(',')
    if(not checknamesindatabase(connection, tablenames_list)):
        print("One or more table names are not in the database.")
        return
    
    combined_fds = getMultipleFDs(connection, tablenames_list)
    closure = computeClosure(attribute_list, combined_fds)
    print("The closure " + ''.join(attribute_list).replace('\'','') + "+ is " + ''.join(closure).replace('\'',''))

def functionality_two(connection):
    fd1names = namestolist(raw_input("Please enter one or more table names to get the functional dependencies set 1 (seperated by comma): "))
    fd2names = namestolist(raw_input("Please enter one or more table names to get the functional dependencies set 2 (seperated by comma): "))
    print("")
    fd1 = getMultipleFDs(connection, fd1names)
    fd2 = getMultipleFDs(connection, fd2names)
    if (checkEqual(fd1, fd2)):
        print("The two sets of functional dependencies are equal!")
    else:
        print("The two sets of functional dependencies are NOT equal!")

def checkAllAttributesSingle(attributelist):
    for attribute in attributelist:
        if (not len(attribute) == 1):
            return False
    return True
    
def namestolist(names):
    outputlist = names.replace(' ', '').split(',')
    return outputlist

def checknamesindatabase(connection, names):
    getnamesquery = """SELECT name FROM SQLITE_MASTER  where name like 'Input_FDs_%'"""
    results = connection.executeQuery(getnamesquery)
    singlecolumn = getSingleColumn("name", results, True)
    for name in names:
        if (name.lower() not in singlecolumn):
            return False
    return True

def getSingleColumn(columnname, table, lower):
    if (columnname is not None):
        list1 = []
        for result in table:
            if(lower):
                list1.append(result[columnname].lower())
            else:
                list1.append(result[columnname])
        return list1
    else:
        return table
    
if  __name__ == "__main__":
    #Unit testing computeClosure
    attribute_list = ['A','B']
    combined_fds = [ [['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']] ]
    computeClosure(attribute_list, combined_fds)
    
    #Unit testing checkEqual
    fdlist1 = [[['M'],['T','N']] , [['P'],['Q','M']]]
    fdlist2 = [ [['M'],['N']] , [['P'],['Q']] , [['P'],['M','T']], [['M','N'],['T']] ]
    print(checkEqual(fdlist1, fdlist2))