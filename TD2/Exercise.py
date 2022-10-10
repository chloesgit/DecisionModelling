from pulp import *

### 1 Introduction to Linear programming with Python

prob = LpProblem("Production optimization", LpMaximize)

x=LpVariable("toy_A",0,None,LpInteger)
y=LpVariable("toy_B",0,None,LpInteger)

# we need to maximize 25*A+20*B
prob += 25*x + 20*y, "Profit; to be maximized"
# the constraint is 20*A + 12*B <= 2000 and 5*A + 5*B <= 9*60
prob += 20*x + 12*y <= 2000
prob += 5*x + 5*y <= 9*60

prob.writeLP("ProductionOptimization.lp")
prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total profit = ", value(prob.objective))

# Conclusion : to maximize the profit, the organization should produce 88 toys A and 20 toys B every day
