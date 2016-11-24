from helper import computeClosure
from main import splitProperties
from macpath import split
from timeit import itertools
T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
Attribute_list = ['A','B','C','D','E','F','G','H','K'] # The Fd u want to check
empty = []
T_2 =[["AB","C"],["AB","D"],["C","A"],["C","D"],["D","A"],["D","E"],["B","F"]]
#===============================================================================
# {A, B, H}+ = {A, B, C, D, E, F, H, K}
# {A, D}+ = {A, D}
# {C, D}+ = {A, C, D, E, F}
# {B, G, H}+ = {A, B, C, D, E, F, G, H, K} <--- Composite minimum candidate key
# {F}+ = {A, D, F}
# {E}+ = {A, D, E, F}
# {B, H}+ = {A, B, C, D, E, F, H, K}
#===============================================================================


def Extraneous_attributes(FD_element,FD):
    FD_Left_side = FD_element[0]
    FD_Right_side = FD_element[1]
    Right_side_str = ''.join(FD_element[1])
    Left_side_combination = itertools.combinations(FD_Left_side,len(FD_Left_side)-1)
    
    if(len(FD_Left_side) == 1):
        return FD
    else:
        
        for single_element_combination in Left_side_combination:
            single_element_combination = list(single_element_combination)
            closure_of_single_element_combination = computeClosure(single_element_combination,FD)
        
            if(Right_side_str in closure_of_single_element_combination):
                FD.remove(FD_element)
                FD.append([single_element_combination,FD_Right_side])
                Extraneous_attributes([single_element_combination,FD_element[1]], FD)
                return FD
        return FD
    
def count_left_hand_side(Single_Fundalmental_dep,Fundalmental_dep):
    count = 0
    for FD in Fundalmental_dep:
        if(Single_Fundalmental_dep == FD[0]):
            count = count + 1
    return count

def redundant(Single_Fundalmental,New_FD,Original_FD):
    
#     print("The FD im testing in redundant is: ", Single_Fundalmental)
    Original_FD_closure = computeClosure(Single_Fundalmental[0],Original_FD)
#     print("The Original closure is: ", Original_FD_closure)
    New_FD.remove(Single_Fundalmental)
#     print("The new FD with the removed is: ", New_FD)
    New_FD_closure = computeClosure(Single_Fundalmental[0],New_FD)
#     print("Now the new closure: " ,New_FD_closure)
    
    if(Original_FD_closure != New_FD_closure):
        New_FD.append(Single_Fundalmental)
        
        return False
    else:
        return True

def minimal_cover(Fundalmental_dep):
    Temp_Fundalmental = []
    closure_array = []
    split_Fundalmental = []
    for Split in Fundalmental_dep:
        split_Fundalmental.append((splitProperties(Split)))
#     print("the split FD: " ,split_Fundalmental)
    
    #Closure of the original 
#     for LHS_FD in split_Fundalmental:
#         closure_array.append(computeClosure(LHS_FD[0],split_Fundalmental))
#     print("The original closure is: " ,closure_array)

    Holder = []
    Holder_2 = []
    
    for FD in split_Fundalmental:
        for i in range(0,len(FD[1])):
            Temp_Fundalmental.append([FD[0],[FD[1][i]]])
            Holder.append([FD[0],[FD[1][i]]])
            Holder_2.append([FD[0],[FD[1][i]]])
#     print("The new split RHS FD : " , Temp_Fundalmental)

    for FD in Holder:
#         print("The FD to use in Extraneous attribute is : ", FD)
        Extraneous_attributes(FD, Temp_Fundalmental)
        Extraneous_attributes(FD, Holder_2)
#     print("The new Extraneous_Fd is : " ,Temp_Fundalmental)
#     print(Holder_2)

#     print(count_left_hand_side(['F'], Temp_Fundalmental))
    for FD in Holder_2:
#         print("The FD im testing is : " , FD)
        if(count_left_hand_side(FD[0],Temp_Fundalmental) > 1):
#             print(" ")
            result = redundant(FD,Temp_Fundalmental,split_Fundalmental)
#             print(result)
#     print(Temp_Fundalmental)
    return(Temp_Fundalmental)


print(minimal_cover(T))
print(minimal_cover(T_2))

def ThreeNF_Decomp(FD):
    U_sets = minimal_cover(FD)
    print(U_sets)
    
#     for FD in U_sets:
#         print(FD)
    
ThreeNF_Decomp(T)