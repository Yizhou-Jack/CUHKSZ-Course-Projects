from cvxpy import *
import numpy as np

team_list = ["BOS", "DAL", "FLA", "GLA", "HOU", "LDN",
             "NYE", "PHI", "SEO", "SFS", "SHD",	"VAL"]

# Problem data.
B = np.matrix([[0, 0,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	1],
               [0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	-1,	0],
               [0,	-1,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0],
               [0,	0, -1,	0,	0,	1,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	-1,	0,	0,	1,	0,	0,	0,	0],
               [-1, 0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0],
               [0, -1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1],
               [1,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0, 0,	0,	0,	0,	0,	0,	1,	-1,	0],
               [0,	0,	0,	0,	0,	1,	0,	-1,	0,	0,	0,	0],
               [0,	0,	0,	0,	-1,	0,	1,	0,	0,	0,	0,	0],
               [0,	0,	0,	-1,	0,	0,	0,	0,	1,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	1,	0,	-1,	0,	0],
               [0,	0,	-1,	0,	0,	0,	0,	0,	1,	0,	0,	0],
               [0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	-1,	0],
               [0,	-1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0, -1],
               [0,	0,	0,	1,	0,	0,	0,	-1,	0,	0,	0,	0],
               [-1, 0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0],
               [0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	-1,	0],
               [0,	-1,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0, -1],
               [0,	0,	0,	-1,	0,	0,	1,	0,	0,	0,	0,	0],
               [-1, 0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0],
               [0,  0,	0,	0,	0,	1,	0,	0,	0,	-1,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	-1,	0],
               [0,	0,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	1],
               [-1, 0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	-1,	1,	0,	0,	0,	0],
               [0,	0,	-1,	0,	1,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	1,	0,	-1,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	-1,	0],
               [0,	1,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	0],
               [1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	1],
               [0,	0,	0,	-1,	1,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	-1,	0,	0,	0,	1],
               [0,	0,	-1,	1,	0,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	1,	0,	0,	0,	0,	-1,	0,	0],
               [0,	-1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	-1,	0],
               [0,	0,	0,	0,	0,	1,	0,	0,	-1,	0,	0,	0],
               [0,	0,	-1,	0,	0,	0,	0,	0,	0,	1,	0,	0],
               [0,	0,	0, 0,	-1,	0,	0,	0,	1,	0,	0,	0],
               [1,	0,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	-1,	0],
               [0,	-1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0],
               [1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, -1],
               [0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	0],
               [0,	0,	0,	1,	0,	0,	0,	0,	0,	-1,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	0,	1],
               [-1, 0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0],
               [0,	0,	-1,	0,	0,	0,	1,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	1,	-1,	0,	0,	0,	0,	0,	0],
               [0,	1,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	0,	1,	-1,	0,	0],
               [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	1],
               [0,	0,	0,	0,	0,	-1,	1,	0,	0,	0,	0,	0],
               [-1, 0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0],
               [0,	0,	-1,	0,	0,	0,	0,	1,	0,	0,	0,	0]])

v = np.array([4, 4,	1, 2, 1, 2,	3, 4, 2, 4,	2, 4,
              1, 4,	4, 4, 3, 1, 4, 4, 2, 1, 4, 1,
              2, 2, 1, 1, 1, 4,	1, 1, 3, 1, 2, 4,
              4, 2, 2, 4, 4, 4, 4, 1, 4, 4, 2, 4,
              1, 2, 3, 4, 3, 2, 2, 1, 4, 1, 1, 1])

one_vector = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

# Construct the problem.
r = Variable(12)
objective = Minimize(sum_squares(B*r - v))
constructs = [r*one_vector = 0]
prob = Problem(objective, constructs)

# The optimal objective is returned by prob.solve()
result = prob.solve()
# The optimal value for x is stored in x.value.
print(x.value)
# The optimal Lagrange multiplier for a constraint
# is stored in constraint.dual_value.
print(constraints[0].dual_value)

print("ranking (worst to best):", team_list[order(x.value)])
