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
    print("super keys are: ",(superKey))
    
    #find minimal key
    minimalKey = superKey[0]
    length = len(superKey[0])
    for key in superKey:
        if len(key) <= length:
            minimalKey = key
    print("Minimal Key is ", minimalKey)
    
    print("Not in BCNF")
    for atr in funcDep:
        if not (isBCNF(attrList, funcDep, atr[0])):
            
            print("LHS: ", atr[0])
            print("AYE");
        
R = ['A','B','C','D','E','F','G','H']
TR = [["ABH","C"], ["A","DE"],["BGH","F"],["F","ADH"],["BH","GE"]]
   
Z =  [[['A','B'],['C']], [['A'],['D']], [['D'],['E']],[['A','C'],['B']]]
Zatt = ['A','B',"C",'D','E']
T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
BCNT(R,TR)
BCNT(Zatt,Z)

