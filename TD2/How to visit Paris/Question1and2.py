from pulp import *
import pandas as pd

### 2 How to visit Paris ?




# creates all variables

#variables of optimization problem
TE=LpVariable("TE",0,1,LpInteger)
ML=LpVariable("ML",0,1,LpInteger)
AT=LpVariable("AT",0,1,LpInteger)
MO=LpVariable("MO",0,1,LpInteger)
JT=LpVariable("JT",0,1,LpInteger)
CA=LpVariable("CA",0,1,LpInteger)
CP=LpVariable("CP",0,1,LpInteger)
CN=LpVariable("CN",0,1,LpInteger)
BS=LpVariable("BS",0,1,LpInteger)
SC=LpVariable("SC",0,1,LpInteger)
PC=LpVariable("PC",0,1,LpInteger)
TM=LpVariable("TM",0,1,LpInteger)
AC=LpVariable("AC",0,1,LpInteger)

#duration [0], appreciations [1], duration [2]

TE_data=[9/2,5,15.5]
ML_data=[3,4,12]
AT_data=[1,3,9.50]
MO_data=[2,2,11]
JT_data=[3/2,3,0]
CA_data=[2,4,10]
CP_data=[5/2,1,10]
CN_data=[2,5,5]
BS_data=[2,4,8]
SC_data=[3/2,1,8.5]
PC_data=[3/4,3,0]
TM_data=[2,2,15]
AC_data=[3/2,5,0]

#creates a dataframe with the distances
data=[[0,3.8,2.1,2.4,3.5,4.2,5,4.4,5.5,4.2,2.5,3.1,1.9],[3.8,0,3.8,1.1,1.3,3.3,1.3,1.1,3.4,0.800,1.7,2.5,2.8],[2.1,3.8,0,3.1,3.0,5.8,4.8,4.9,4.3,4.6,2.2,4.4,1],[2.4,1.1,3.1,0,0.9,3.1,2.5,2,3.9,1.8,1,2.3,2.1],[3.5,1.3,3.0,0.9,0,4.2,2,2.4,2.7,2,1,3.4,2.1],[4.2,3.3,5.8,3.1,4.2,0,3.5,2.7,6.5,2.6,3.8,1.3,4.9],[5,1.3,4.8,2.5,2,3.5,0,0.85,3.7,0.9,2.7,3.4,3.8],[4.4,1.1,4.9,2,2.4,2.7,0.85,0,4.5,0.4,2.8,2.7,3.9],[5.5,3.4,4.3,3.9,2.7,6.5,3.7,4.5,0,4.2,3.3,5.7,3.8],[4.2,0.8,4.6,1.8,2,2.6,0.9,0.4,4.2,0,2.5,2.6,3.6],[2.5,1.7,2.2,1,1,3.8,2.7,2.8,3.3,2.5,0,3,1.2],[3.1,2.5,4.4,2.3,3.4,1.3,3.4,2.7,5.7,2.6,3,0,2.1],[1.9,2.8,1,2.1,2.1,4.9,3.8,3.9,3.8,3.6,1.2,2.1,0]]
columns=["TE","ML","AT","MO","JT","CA","CP","CN","BS","SC","PC","TM","AC"]
index=["TE","ML","AT","MO","JT","CA","CP","CN","BS","SC","PC","TM","AC"]
distance = pd.DataFrame(data=data,index=index,columns=columns)

#creates a dictionnary gathering monument name, optimization variable and data on this monument
dic={"TE":[TE,TE_data],"ML":[ML,ML_data],"AT":[AT,AT_data],"MO":[MO,MO_data],"JT":[JT,JT_data],"CA":[CA,CA_data],"CP":[CP,CP_data],"CN":[CN,CN_data],"BS":[BS,BS_data],"SC":[SC,SC_data],"PC":[PC,PC_data],"TM":[TM,TM_data],"AC":[AC,AC_data]}


#implements the solver
def solve_pb(problem):
    problem.writeLP("ListVisit1Optimization.lp")
    problem.solve()
    visited_Sites = []
    for v in problem.variables():
        if v.varValue == 1:
            visited_Sites.append(v.name)
    print("Number of visited sites = ", value(problem.objective))
    print("Visited sites = ", visited_Sites)
    return visited_Sites

#test if two lists are equals
def areListEqual(list1,list2):
    #we know that the sites will systematically appear in the same order
    L1,L2 = len(list1),len(list2)
    if L1 != L2:
        return False
    else:
        for i in range(L1):
            if list1[i]!=list2[i]:
                return False
        return True




## Question 1

prob2=LpProblem("ListVisit1", LpMaximize)
# value to maximize
prob2 += TE + ML + AT + MO + JT + CA + CP + CN + BS + SC + PC + TM + AC, "Number of visited sites; to be maximized"

# constraints : duration <= 12
prob2 += TE*TE_data[0] + ML*ML_data[0] + AT*AT_data[0] + MO*MO_data[0] + JT*JT_data[0] + CA*CA_data[0] + CP*CP_data[0] + CN*CN_data[0] + BS*BS_data[0] + SC*SC_data[0] + PC*PC_data[0] + TM*TM_data[0] + AC*AC_data[0] <= 12
prob2 += TE*TE_data[2] + ML*ML_data[2] + AT*AT_data[2] + MO*MO_data[2] + JT*JT_data[2] + CA*CA_data[2] + CP*CP_data[2] + CN*CN_data[2] + BS*BS_data[2] + SC*SC_data[2] + PC*PC_data[2] + TM*TM_data[2] + AC*AC_data[2] <= 65

visited_Sites1 = solve_pb(prob2)
#ListVisit1: ['AC', 'AT', 'BS', 'CA', 'CN', 'PC', 'SC']

## Question 2

#we create a function that automatically create the "basic" problem with the compulsary constraints
def create_prob():
    prob3=LpProblem("ListVisit2", LpMaximize)
    # value to maximize
    prob3 += TE + ML + AT + MO + JT + CA + CP + CN + BS + SC + PC + TM + AC, "Number of visited sites; to be maximized"
    # constraints : 
    prob3 += TE*TE_data[0] + ML*ML_data[0] + AT*AT_data[0] + MO*MO_data[0] + JT*JT_data[0] + CA*CA_data[0] + CP*CP_data[0] + CN*CN_data[0] + BS*BS_data[0] + SC*SC_data[0] + PC*PC_data[0] + TM*TM_data[0] + AC*AC_data[0] <= 12
    prob3 += TE*TE_data[2] + ML*ML_data[2] + AT*AT_data[2] + MO*MO_data[2] + JT*JT_data[2] + CA*CA_data[2] + CP*CP_data[2] + CN*CN_data[2] + BS*BS_data[2] + SC*SC_data[2] + PC*PC_data[2] + TM*TM_data[2] + AC*AC_data[2] <= 65
    return prob3


# question 2 (a)

def distanceinf1(distance):
    L=[]
    for x in distance.columns:
        for y in distance.index:
            if distance[x][y]<=1:
                L.append( [x,y])
    return(L)

#pref1:
def pref1(problem):
    closenodes=distanceinf1(distance)
    for i in range (len(closenodes)):
        problem += dic[closenodes[i][0]][0]==dic[closenodes[i][1]][0]
    return problem

#compares the list obtained with ListVisit1
def test_pref1():
    prob = create_prob()
    prob = pref1(prob)
    visited_Sites = solve_pb(prob)
    print("pref 1")
    return areListEqual(visited_Sites1,visited_Sites)

#pref2:
def pref2(problem):
    problem += TE + CA >= 2
    return problem

 #compares the list obtained with ListVisit1   
def test_pref2():
    prob = create_prob()
    prob = pref2(prob)
    visited_Sites = solve_pb(prob)
    print("pref 2")
    return (areListEqual(visited_Sites1,visited_Sites))

#pref3:
def pref3(problem):
    problem += CN + SC <= 1
    return problem
    
    #compares the list obtained with ListVisit1
def test_pref3():
    prob = create_prob()
    prob = pref3(prob)
    visited_Sites = solve_pb(prob)
    print("pref 3")
    return (areListEqual(visited_Sites1,visited_Sites))

#pref4:
def pref4(problem):
    problem += TM >= 1
    return problem

#compares the list obtained with ListVisit1
def test_pref4():
    prob = create_prob()
    prob = pref4(prob)
    visited_Sites = solve_pb(prob)
    print("pref 4")
    return areListEqual(visited_Sites1,visited_Sites)

#pref5:
def pref5(problem):
    problem += (ML-CP) <= 0
    return problem

#compares the list obtained with ListVisit1
def test_pref5():
    prob = create_prob()
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    print("pref 5")
    return areListEqual(visited_Sites1,visited_Sites)

proposedVisitList = []
proposedVisitList.append(test_pref1())
proposedVisitList.append(test_pref2())
proposedVisitList.append(test_pref3())
proposedVisitList.append(test_pref4())
proposedVisitList.append(test_pref5())

print(proposedVisitList)
#[False, False, False, False, True]


# for the following, we are storng the lists proposed in an array called 'Solutions'
Solutions = []




# 2 (b)

def solve2_b():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref2(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_b())
Solutions.append(solve2_b())
#solution:  ['AC', 'AT', 'CA', 'TE', 'TM']

# 2 (c)

def solve2_c():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref3(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_c())
Solutions.append(solve2_c())
#solution:  ['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']

# 2 (d)

def solve2_d():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref4(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_d())
Solutions.append(solve2_d())
#solution:  ['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']

# 2 (e)

def solve2_e():
    prob = create_prob()
    prob = pref2(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_e())
Solutions.append(solve2_e())
#solution:  ['AC', 'AT', 'CA', 'JT', 'PC', 'TE']

# 2 (f)

def solve2_f():
    prob = create_prob()
    prob = pref3(prob)
    prob = pref4(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_f())
Solutions.append(solve2_f())
#solution:  ['AC', 'AT', 'BS', 'CA', 'PC', 'SC', 'TM']

# 2 (g)

def solve2_g():
    prob = create_prob()
    prob = pref4(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_g())
Solutions.append(solve2_g())
#solution:  ['AC', 'AT', 'BS', 'CN', 'PC', 'SC', 'TM']

# 2 (h)

def solve2_h():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref4(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_h())
Solutions.append(solve2_h())
#solution:  ['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']

# 2 (i)

def solve2_i():
    prob = create_prob()
    prob = pref2(prob)
    prob = pref3(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_i())
Solutions.append(solve2_i())
#solution:  ['AC', 'AT', 'CA', 'JT', 'PC', 'TE']

# 2 (j)

def solve2_j():
    prob = create_prob()
    prob = pref2(prob)
    prob = pref3(prob)
    prob = pref4(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_j())
Solutions.append(solve2_j())
#solution:  ['AC', 'AT', 'CA', 'PC', 'TE', 'TM']

# 2 (k)

def solve2_k():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref2(prob)
    prob = pref4(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_k())
Solutions.append(solve2_k())
#solution:  ['AC', 'AT', 'CA', 'TE', 'TM']

# 2 (l)

def solve2_l():
    prob = create_prob()
    prob = pref1(prob)
    prob = pref2(prob)
    prob = pref3(prob)
    prob = pref4(prob)
    prob = pref5(prob)
    visited_Sites = solve_pb(prob)
    return visited_Sites
print(solve2_l())
Solutions.append(solve2_l())
#solution:  ['AC', 'AT', 'CA', 'TE', 'TM']

# 2 (m)

print(proposedVisitList)

for i,solution in enumerate(Solutions):
    print('\nfor 2('+str(chr(97+1+i))+')')
    print('solution: ',solution)
    print(areListEqual(visited_Sites1,solution))
print('\nListVisit1 : ',visited_Sites1)

#None of the proposed solution matches the ListVisit1, but this is consistent with the fact that only preference5 leads to the same list as ListVisit1
