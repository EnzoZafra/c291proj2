import helper
import main
import sqlcontroller as controller
from timeit import itertools

#If there is no Super_key in R then we create one by making a list of possible combinations and computing closure
def create_super_key(FD,Attribute_list,size,Super_key_list):
    combination = itertools.combinations(Attribute_list,size)
    Super_keys = Super_key_list

    for comb in combination:
        result = helper.computeClosure(list(comb),FD)
        if(sorted(result) == Attribute_list):
            if(list(comb) not in Super_keys):
                Super_keys.append(list(comb))
                return Super_keys
    return create_super_key(FD, Attribute_list, size + 1,Super_keys)

#Grab all possible super_keys in our R
def get_super_key(FD,Attribute_list):
    split_Fundalmental = []
    Super_keys = []
    for Split in FD:
        split_Fundalmental.append((main.splitProperties(Split)))
    for Element in split_Fundalmental:
        result = helper.computeClosure(Element[0],split_Fundalmental)
        if((sorted(result) == Attribute_list)):
            Super_keys.append(Element[0])
            return Super_keys
    return False

#This is where we check if our FD list contains our original super_key 
def check_if_super_key_in_FD(FD,super_key):
    result = False
    for FD_element in FD:
        if(FD_element[0] in super_key):
            result = True
            return result
    return result

#This is where we check the LHS of our FD's to see if theyre redundant
def Extraneous_attributes(FD_element,FD):
    FD_Left_side = FD_element[0]
    FD_Right_side = FD_element[1]
    Right_side_str = ''.join(FD_element[1])
    Left_side_combination = itertools.combinations(FD_Left_side,len(FD_Left_side)-1)
    #If our FD is just a single one EX: A --> D then its not redundant
    if(len(FD_Left_side) == 1):
        return FD
    #However if our FD is more than one on the LHS EX: ABC --> D then we check every possible combination to see which is redundant
    else:
        for single_element_combination in Left_side_combination:
            single_element_combination = list(single_element_combination)
            closure_of_single_element_combination = helper.computeClosure(single_element_combination,FD)
            
            #Now to see if redundant we check if our Right hand side is in our new closure of the new posibility
            if(Right_side_str in closure_of_single_element_combination):
                FD.remove(FD_element)
                FD.append([single_element_combination,FD_Right_side])
                Extraneous_attributes([single_element_combination,FD_element[1]], FD)
                return FD
        return FD
    
#This is where we check how many times the LHS FD occurs in our list
def count_left_hand_side(Single_Fundalmental_dep,Fundalmental_dep):
    count = 0
    for FD in Fundalmental_dep:
        if(Single_Fundalmental_dep == FD[0]):
            count = count + 1
    return count

#This is where we check to see which FD's a redundant for example A-->D,A-->B we remove one and then compute the closure
def redundant(Single_Fundalmental,New_FD,Original_FD):
    Original_FD_closure = helper.computeClosure(Single_Fundalmental[0],Original_FD)
    New_FD.remove(Single_Fundalmental)
    New_FD_closure = helper.computeClosure(Single_Fundalmental[0],New_FD)
        
    if(Original_FD_closure != New_FD_closure):
        New_FD.append(Single_Fundalmental)
        return False
    else:
        return True

#Computing the minimal cover
def minimal_cover(Fundalmental_dep):
    Temp_Fundalmental = []
    split_Fundalmental = []
    for Split in Fundalmental_dep:
        split_Fundalmental.append((main.splitProperties(Split)))
    
    #Make these as placeholders so when we edit our actual list it wont edit these
    Holder = []
    Holder_2 = []
    
    for FD in split_Fundalmental:
        for i in range(0,len(FD[1])):
            Temp_Fundalmental.append([FD[0],[FD[1][i]]])
            Holder.append([FD[0],[FD[1][i]]])
            Holder_2.append([FD[0],[FD[1][i]]])
    
    #Check if LHS elements are redundant
    for FD in Holder:
        Extraneous_attributes(FD, Temp_Fundalmental)
        Extraneous_attributes(FD, Holder_2)
    
    #Check if our FD's are redundant
    for FD in Holder_2:
        if(count_left_hand_side(FD[0],Temp_Fundalmental) > 1):
            redundant(FD,Temp_Fundalmental,split_Fundalmental)
    return(Temp_Fundalmental)
#Get all elements in a FD combination EX : ABC -> D would make a list of [A,B,C,D]
def Get_all_Attributes(FD):
    Attribute_list = []
    
    for FD_ele in FD:        
        for i in range(0,len(FD_ele[0])):
            if(FD_ele[0][i] not in Attribute_list):
                Attribute_list.append(FD_ele[0][i])
        for j in range(0,len(FD_ele[1])):
            if(FD_ele[1][j] not in Attribute_list):
                Attribute_list.append(FD_ele[1][j])
    return Attribute_list

    #Where we now do our decomposition
def ThreeNF_Decomp(Attribute_list, FD):
    
#First we have to make it into a minimal cover
    U_sets = minimal_cover(FD)
    
#Grab our original super key from the Relation    
    Original_superkey = get_super_key(FD, Attribute_list)
    
    #PlaceHolders/weight
    U_sets_split = []
    
    LHS_done_so_far = []
    
    #This is where we group all our fd's together for EX: A-->D , BH -->K , BH --> C would return {A-->D},{BH-->K,BH-->C}
    count = 0;
    for FD in U_sets:
        
        if(FD[0] in LHS_done_so_far):
            continue
        else:
            LHS_done_so_far.append(FD[0])
            U_sets_split.append([])
            for fd in U_sets:
                Temp = []
                if fd[0] == FD[0]:
                    Temp.append(fd[0])
                    Temp.append(fd[1])
                    U_sets_split[count].append(Temp)

            count+=1
    #This is where now we put all the attributes together with the FD EX: A-->D,A-->B would return {A,D,B; A-->D,A-->B}
    Relation = []
    for i in U_sets_split:
        Relation.append((Get_all_Attributes(i),i))
     
    #Now this is step 4 where we check if theres a super key or not inside
    if(Original_superkey == False):
        size = 0
        Super_key_list = []
        new_super_key = create_super_key(U_sets, Attribute_list,size,Super_key_list)
        for i in new_super_key:
            Relation_key = i, []
            Relation.append(Relation_key)        
    else:
        check = check_if_super_key_in_FD(U_sets,Original_superkey)
        if(check == False):
            for i in Original_superkey:                
                Relation_key = i,[]
                Relation.append(Relation_key)
    dict_relation = {}
    for i in Relation:
        for k in i:
            dict_relation[''.join(i[0])] = k
    return dict_relation

def threenfInterface(connection, attrList, funcDep, name):
    newtables = ThreeNF_Decomp(attrList, funcDep)
    controller.createTables(connection, newtables, name)
    selection = raw_input("Would you like to decompose the original table instance according to the schema decomposition? [Y/N] ").lower()
    if (selection == "y"):
        controller.moveData(connection, newtables, name)
    
if  __name__ == "__main__":
    
    # UNIT TESTING
        #===============================================================================
    # {A, B, H}+ = {A, B, C, D, E, F, H, K}
    # {A, D}+ = {A, D}
    # {C, D}+ = {A, C, D, E, F}
    # {B, G, H}+ = {A, B, C, D, E, F, G, H, K} <--- Composite minimum candidate key
    # {F}+ = {A, D, F}
    # {E}+ = {A, D, E, F}
    # {B, H}+ = {A, B, C, D, E, F, H, K}
    #===============================================================================
    
    T_1 = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]
    Attribute_list_1 = ['A','B','C','D','E','F','G','H','K'] # The Fd u want to check
    Attribute_list_2 = ['A','B','C','D','E','F']
    Attribute_list_3 = ['A','B','C','D']
    T_2 =[["AB","C"],["AB","D"],["C","A"],["C","D"],["D","A"],["D","E"],["B","F"]]
    T_3 = [['A','B'],['C','D']]
    
#     print(minimal_cover(T))
#     print(minimal_cover(T_2))
    print(ThreeNF_Decomp(Attribute_list_1,T_1))
    print(ThreeNF_Decomp(Attribute_list_2,T_2))
    print(ThreeNF_Decomp(Attribute_list_3,T_3))
# T = [[['A'],['B']],[['B'],['C']]]
