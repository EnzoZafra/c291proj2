import main
import sqlcontroller as sql

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
    print(closure)
    return closure;
            
def getMultipleFDs(connection, list_names):
    combinedFDs = []
    for name in list_names:
        fd = sql.getFunctionalDependencies(connection, main.regexTableName(name))
        combinedFDs.append(main.splitProperties(fd))
    return combinedFDs

def functionality_one(connection):
    attribute_input = raw_input("Please enter the list of attributes [i.e = 'A,B,C']: ")
    tablenames_input = raw_input("Please enter the list of table names to get the functional dependencies from: ")
    tablenames_list = tablenames_input.split(',')
    
    combinedFDs = getMultipleFDs(connection, tablenames_list)
    attribute_list = attribute_input.split(',')

if  __name__ == "__main__":
    #Unit testing computeClosure
    attribute_list = ['A','B']
    combined_fds = [ [['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']] ]
    computeClosure(attribute_list, combined_fds)