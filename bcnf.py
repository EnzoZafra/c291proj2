from helper import *
import main
import sqlcontroller as controller

#attribute_list = ['A','B']
   # combined_fds = [ [['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']] ]
   #computeClosure(attribute_list, combined_fds):


#===============================================================================
# This finds if it is SUPER KEY
#  for atr in Z:
#      print(computeClosure(atr[0],Z))
#      print(set(computeClosure(atr[0], Z)).issuperset(set(Zatt)))
#===============================================================================



# isBCNF(["AB"] [all funcdeps])
def isBCNF(attrList, funcDep, atr):
    
    if (set(computeClosure(atr,funcDep)).issuperset(attrList)):
        return True
    return False

def isDependencyPreserved():
    return -1

def BCNT(attrList, funcDep):
#     print(isBCNF(attrList,funcDep))
    superKey = []
    for atr in funcDep:
        if (set(computeClosure(atr[0],funcDep)).issuperset(attrList)):
            superKey.append(atr[0])
#     print("super keys are: ",(superKey))
    
    
    #===========================================================================
    # find minimal key
    #  if superKey[0] != []:
    #      minimalKey = superKey[0]
    #      length = len(superKey[0])
    #      for key in superKey:
    #          if len(key) <= length:
    #              minimalKey = key
    #      print("Minimal Key is ", minimalKey)
    #===========================================================================
    
    relation = []
    relation.append(attrList)
    
    functDepend = list(funcDep)
    newFDs = []
    R = {}
    
    splitCount = 1
#     print("Initial Relation: ", attrList)
#     print("Initial FDs: ", funcDep)
    for atr in funcDep:
#         print("Atr: ", atr)
        if atr in functDepend:
            newFDs.append(atr)
            if not (isBCNF(attrList, funcDep, atr[0])):
                relation.append([])
#                 print("LHS: ", atr[0])
                for Attribute in atr[0]:
                    relation[splitCount].append(Attribute)
#                 print("RHS: ", atr[1])
                for Attribute in atr[1]:
                    relation[0].remove(Attribute)
                    relation[splitCount].append(Attribute)
                    
                functDepend.remove(atr)
                for FD in functDepend:
                    for attriRemoved in atr[1]:
                        if attriRemoved in FD[1]:
#                             print("at remove: ", attriRemoved)
#                             print(FD[1])
                            FD[1].remove(attriRemoved)
#                 print("Relation split: ",relation)    
#                 print("Remaining FDs: ", functDepend)
                splitCount += 1
    count = -1
#     print("NEW FDS: " , newFDs)
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

            R["".join(table)] = []
    print(R)
    
R = ['A','B','C','D','E','F','G','H']
TR = [[['A','B','H'],['C']], [['A'],['D','E']],[['B','G','H'],['F']],[['F'],['A','D','H']],[['B','H'],['G','E']]]
Z = [[['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']]]
#   [[['A','B'], ['C']], [['C'],['D']] ]
Zatt = ['A','B',"C",'D','E']
T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
BCNT(R,TR)
print()
BCNT(Zatt,Z)    
Bank = ['B','C','A','N','L','M']
BankFD = [[['B'],['A','C']],[['L'],['M','B']]]
BCNT(Bank,BankFD)
R = ['A','B','C','D','E','F','G','H','K']
T = [[['A', 'B', 'H'], ['C', 'K']], [['A'], ['D']], [['C'], ['E']], [['B', 'G', 'H'], ['F']], [['F'], ['A', 'D']], [['E'], ['F']], [['B', 'H'], ['E']]]
T1 = [[['B','H'],['E']],[['A', 'B', 'H'], ['C', 'K']], [['A'],['D']], [['E'],['F']],[['F'],['A']]]
BCNT(R,T)
# print(checkEqual(T,T1))
R = ['A','B','C','D']
T = [[['A'],['B']],[['B'],['C']]]
BCNT(R,T)
# print(checkEqual(T,T))