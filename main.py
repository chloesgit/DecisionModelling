import pandas as pd
import matplotlib.pyplot as plt


#converts an excel file to a list of rows
def convert_excel_to_graph(file_name):
    excelFile = pd.read_excel (file_name, header=None)
    excelFile.to_csv ("file_to_csv.csv", index = None)
    dataframeObject = pd.DataFrame(pd.read_csv("file_to_csv.csv"))
    list=dataframeObject.values.tolist()
    return list

#checks whether a matrix is complete
def CompleteCheck(rel):
    n = len(rel)
    for i in range(n):
        for j in range(n):
            x,y = rel[i],rel[j]
            if x[j] == 0 and y[i] == 0:
                return False
    return True

#checks whether a matrix is reflexive
def ReflexiveCheck(rel):
    n = len(rel)
    for i in range(n):
        if rel[i][i]==0:
            return False
    return True

#checks whether a matrix is asymmetric
def AsymmetricCheck(rel):
    n = len(rel)
    for i in range(n):
        for j in range(n):
            if rel[i][j]==1 and rel[j][i]==1:
                return False
    return True

#checks whether a matrix is antisymmetric
def AntisymmetricCheck(rel):
    n = len(rel)
    for i in range(n):
        for j in range(n):
            if rel[i][j]==1 and rel[j][i]==1 and i!=j:
                return False
    return True

#checks whether a matrix is transitive
def TransitiveCheck(rel):
    n = len(rel)
    for i in range(n):
        for j in range(n):
            if rel[i][j]==1:
                for k in range(n):
                    if rel[j][k]==1 and rel[i][k]!=1:
                        return False
    return True

#checks whether a matrix is negative transitive
def NegativetransitiveCheck(rel):
    n = len(rel)
    for i in range(n):
        for j in range(n):
            if rel[i][j]==0:
                for k in range(n):
                    if rel[j][k]==0 and rel[i][k]==1:
                        return False
    return True

#complete order is complete, antisymmetric and transitive
def CompleteOrderCheck(rel):
    if CompleteCheck(rel) and TransitiveCheck(rel) and AntisymmetricCheck(rel):
        return True
    return False

#complete pre order is complete, transitive and reflexive
def CompletePreOrderCheck(rel):
    if CompleteCheck(rel) and TransitiveCheck(rel) and ReflexiveCheck(rel):
        return True
    return False

#computes the asymmetric part of the relation 
def StrictRelation(rel):
    n = len(rel)
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if rel[i][j]*rel[j][i] == 0 :
                res[i][j],res[j][i]=rel[i][j],rel[j][i]
    return res

#computes the symmetric part of the relation 
def IndifferenceRelation(rel):
    n = len(rel)
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if rel[i][j] == 1 and rel[j][i] == 1:
                res[i][j],res[j][i]=1,1
    return res

#returns the topological order of a relation
def Topologicalsorting(rel):
    n = len(rel)
    rel2=list(rel)#copy of rel
    res,dominated,deleted = [],[],[]
    for i in range(n):
        rel2[i][i] = 0
    stop = False
    while stop == False:
        for i in range(n):
            if i not in deleted and 1 not in rel2[i]:
                dominated.append(i)
        if dominated == []:
            stop = True
            break
        else:
            res.append(list(dominated))
            
            for i in dominated:
                for j in range(n):
                    rel2[j][i]=0
                deleted.append(i)
            dominated = []
            # print('\n')
            # print('deleted:',deleted)
            # print('rel2',rel2)
            # print('res:',res)
    return res

rel=convert_excel_to_graph("matrix.xlsx")
print ("list",convert_excel_to_graph("matrix.xlsx"))
print("complete",CompleteCheck(rel))
print("reflexive",ReflexiveCheck(rel))
print("asymmetric",AsymmetricCheck(rel))
print("antisymmetric",AntisymmetricCheck(rel))
print("transitive",TransitiveCheck(rel))
print("negative transitive",NegativetransitiveCheck(rel))
print("complete order",CompleteOrderCheck(rel))
print("complete preorder",CompletePreOrderCheck(rel))
print("strict relation",StrictRelation(rel))
print("indifference relation",IndifferenceRelation(rel))
print("topological sorting",Topologicalsorting(rel))
