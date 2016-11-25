from helper import *
import main
import sqlcontroller as controller


#===============================================================================
# #This function checks if the attribute list is in BCNF form
#===============================================================================
def isBCNF(attrList, funcDep, atr):
    
    if (set(computeClosure(atr,funcDep)).issuperset(attrList)):
        return True
    return False

def isSuperKey(attributeList, funcDep, attrList):
    return set(computeClosure(attributeList,funcDep)).issuperset(attrList)

#===============================================================================
# #Function used to decompose the schema
# #attrList is the list of all the attributes
# #funcDep is the all the functional dependencies for this relation
#===============================================================================
def BCNT(attrList, funcDep):
#     print(isBCNF(attrList,funcDep))

    #Search for all the super keys
    superKey = []
    for FD in funcDep:
        if (isSuperKey(FD[0],funcDep,attrList)):
            superKey.append(FD[0])
    print("super:" , superKey)
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
                print("fd: ",fd)
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
#             print(set(tempList))
#             print("table: ", set(table))
            if set(tempList).issuperset(set(table)):
                R["".join(table)] = FD
#         print(R.get("".join(table)))
        if not R.get("".join(table),[]):
            print("".join(table))
            R["".join(table)] = []
    print("orignial:", funcDep)
#     for FD in newFDs:
#         print(FD)
    print(newFDs)
    print(checkEqual(funcDep,newFDs))
    print(R)
    
     
R = ['A','B','C','D','E','F','G','H']
TR = [[['A','B','H'],['C']], [['A'],['D','E']],[['B','G','H'],['F']],[['F'],['A','D','H']],[['B','H'],['G','E']]]
Z = [[['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']]]
# #   [[['A','B'], ['C']], [['C'],['D']] ]
# Zatt = ['A','B',"C",'D','E']
# T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
# BCNT(R,TR)
# BCNT(Zatt,Z)    
# Bank = ['B','C','A','N','L','M']
# BankFD = [[['B'],['A','C']],[['L'],['M','B']]]
# BCNT(Bank,BankFD)
# R = ['A','B','C','D','E','F','G','H','K']
# T = [[['A', 'B', 'H'], ['C', 'K']], [['A'], ['D']], [['C'], ['E']], [['B', 'G', 'H'], ['F']], [['F'], ['A', 'D']], [['E'], ['F']], [['B', 'H'], ['E']]]
# T1 = [[['B','H'],['E']],[['A', 'B', 'H'], ['C', 'K']], [['A'],['D']], [['E'],['F']],[['F'],['A']]]
R = ['A','B','C','D','E','F','G','H']
T = [[['A', 'B', 'H'], ['C']], [['A'], ['D','E']], [['B', 'G', 'H'], ['F']], [['F'], ['A', 'D','H']], [['B', 'H'], ['G','E']]]
# print("test",checkEqual(T,T1))
BCNT(R,T)
# print(checkEqual(T,T1))
# R = ['A','B','C','D']
# T = [[['A'],['B']],[['B'],['C']]]
# R = ['A','B','C']
# T = [[['A'],['B']],[['B'],['C']],[['C'],['B']]]

# BCNT(R,T)
# print(checkEqual(T,T))
# R = ['A','B','C','F','G','H']
# T = [[['A','B','H'],['C']],[['B','G','H'],['F']],[['F'],['A','H']],[['B','H'],['G']]]
# BCNT(R,T)
