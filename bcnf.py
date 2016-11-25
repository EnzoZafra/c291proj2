import helper
import main
import sqlcontroller as controller

#===============================================================================
# #This function checks if the attribute list is in BCNF form
#===============================================================================
def isBCNF(attrList, funcDep, atr):
    
    if (set(helper.computeClosure(atr,funcDep)).issuperset(attrList)):
        return True
    return False

def isSuperKey(attributeList, funcDep, attrList):
    return set(helper.computeClosure(attributeList,funcDep)).issuperset(attrList)

#===============================================================================
# #Function used to decompose the schema
# #attrList is the list of all the attributes
# #funcDep is the all the functional dependencies for this relation
#===============================================================================

def splitWholeList(funcDep):
    output = []
    for fd in funcDep:
        output.append(main.splitProperties(fd))
    return output

def BCNT(attrList, unsplitfd):
    funcDep = splitWholeList(unsplitfd)
    #Search for all the super keys
    superKey = []
    for FD in funcDep:
        if (isSuperKey(FD[0],funcDep,attrList)):
            superKey.append(FD[0])
    
    #Variable to hold the attribute Lists R1,R2,R3
    relation = []
    relation.append(attrList)
    #Temporary variable for funcDep that gets customized
    functDepend = list(funcDep)
    #Variable to store the FDs of the split relations
    newFDs = []
    #Dictionary used to put into Relation form
    R = {}
    
    #Counter for R1,R2,R3 leaving the first index the original that loses attributes
    splitCount = 1

    for fd in funcDep:
        
        if fd in functDepend:
            
            #If the LHS of FD is not in BCNF, split
            if not (isBCNF(attrList, funcDep, fd[0])):
                newFDs.append(fd)
                
                relation.append([])
                #Add the attributes on LHS to Ri
                for Attribute in fd[0]:
                    relation[splitCount].append(Attribute)
                #Add attributes on RHS to Ri and remove attributes from original
                for Attribute in fd[1]:
                    relation[0].remove(Attribute)
                    relation[splitCount].append(Attribute)
                #Removed this FD
                functDepend.remove(fd)
                #Remove the removed attributes from remaining FDs
                for FD in functDepend:
                    for attriRemoved in fd[1]:
                        if attriRemoved in FD[1]:
                            FD[1].remove(attriRemoved)
                # Check if removed attribute is in LHS of FD
                for i in functDepend:
                    for j in i[0]:
                        if not set(j).issubset(relation[0]):
                            functDepend.remove(i)
                            break
                #increment counter
                splitCount += 1
    #To put relation and FD together as a dictionary
    for table in relation:
        for FD in newFDs:
            tempList = []
            for attr in FD[0]:
                tempList.append(attr)
            for attr in FD[1]:
                tempList.append(attr)
            if set(tempList).issuperset(set(table)):
                R["".join(table)] = [FD]
        if not R.get("".join(table),[]):
            
            R["".join(table)] = []
    
    if (helper.checkEqual(funcDep, newFDs)):
        print("The resulting BCNF decomposition is dependency preserving.")
    else:
        print("The resulting BCNF decomposition is NOT dependency preserving")
    return R

def BCNFInterface(connection, attrList, funcDep, name):
    newtables = BCNT(attrList, funcDep)
    controller.createTables(connection, newtables, name)
    selection = raw_input("Would you like to decompose the original table instance according to the schema decomposition? [Y/N] ").lower()
    if (selection == "y"):
        controller.moveData(connection, newtables, name)
    
if __name__ == "__main__":
    ## UNIT testing
    R = ['A','B','C','D','E','F','G','H']
    TR = [[['A','B','H'],['C']], [['A'],['D','E']],[['B','G','H'],['F']],[['F'],['A','D','H']],[['B','H'],['G','E']]]
    Z = [[['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']]]
    #   [[['A','B'], ['C']], [['C'],['D']] ]
    Zatt = ['A','B',"C",'D','E']
    T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
    BCNT(R,TR)
    BCNT(Zatt,Z)    
    Bank = ['B','C','A','N','L','M']
    BankFD = [[['B'],['A','C']],[['L'],['M','B']]]
    BCNT(Bank,BankFD)
    R = ['A','B','C','D','E','F','G','H','K']
    T = [[['A', 'B', 'H'], ['C', 'K']], [['A'], ['D']], [['C'], ['E']], [['B', 'G', 'H'], ['F']], [['F'], ['A', 'D']], [['E'], ['F']], [['B', 'H'], ['E']]]
    T1 = [[['B','H'],['E']],[['A', 'B', 'H'], ['C', 'K']], [['A'],['D']], [['E'],['F']],[['F'],['A']]]
    print("test",helper.checkEqual(T,T1))
    BCNT(R,T)
    # print(checkEqual(T,T1))
    R = ['A','B','C','D']
    T = [[['A'],['B']],[['B'],['C']]]
    BCNT(R,T)
    print(helper.checkEqual(T,T))
    R = ['A','B','C','F','G','H']
    T = [[['A','B','H'],['C']],[['B','G','H'],['F']],[['F'],['A','H']],[['B','H'],['G']]]
    BCNT(R,T)
