T = [["ABH","CK"],["A","D"],["C","E"],["BGH","F"],["F","AD"],["E","F"],["BH","E"]]

#===============================================================================
# print(T)
# print(len(T[1]))
# k = T[0]
# print(k[1][1])
#===============================================================================


def minimal_cover(Fundalmental_dep):
    Temp_Fundalmental = []
    Clousure_Fundalmental_dep = []
    for closure_FD in Fundalmental_dep:
        print(closure_FD[0]) 
        #Closure_Fundalmental_dep.append(closure_FD[0])
    for FD in Fundalmental_dep:
            for i in range(0,len(FD[1])):
                Temp_Fundalmental.append((FD[0],FD[1][i]))
    #print(Temp_Fundalmental)
    
minimal_cover(T)

