from itertools import product
from mip import Model, xsum, BINARY,minimize, INTEGER
"""
n = 10  # Atividades

p = [0, 3, 2, 5, 4, 2, 3, 4, 2, 4, 6, 0]

u = [[0, 0], [5, 1], [0, 4], [1, 4], [1, 3], [3, 2], [3, 1], [2, 4],
     [4, 0], [5, 2], [2, 5], [0, 0]]

c = [6, 8]

S = [[0, 1], [0, 2], [0, 3], [1, 4], [1, 5], [2, 9], [2, 10], [3, 8], [4, 6],
     [4, 7], [5, 9], [5, 10], [6, 8], [6, 9], [7, 8], [8, 11], [9, 11], [10, 11],[6,11]]"""

"""n = 6
p = [0,2,3,3,2,4,3,0]
u = [[0,0,0,0],[0,0,0,0],[2,1,1,1],[4,3,3,3],[1,2,2,2],[3,1,1,1],[5,3,0,0],[0,0,0,0]]
c = [5,5,5,5]
S = [[0,1],[1,3],[2,3],[3,4],[4,5],[5,7],[6,7]]
w = [1,1,1,2,1,1,1,1]
d = [0,1,2,4,10,21,25,38]"""

n = 14
p = [0,1,2,2,3,2,3,19,2,10,3,5,9,6,9,0]
c = [160,160,160,160,160]
S = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15]]
d = [61,71,81,91,111,321,521,321,321,621,721,821,821,821,821,831]
u = [[0,0,0,0,0],[4,1,0,5,0],[5,0,0,0,0],[4,1,1,5,10],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0]]
(R, J, T) = (range(len(c)), range(len(p)), range(sum(p)+1))

            
model = Model()
x = [[model.add_var(name="x({},{})".format(j, t), var_type=BINARY) for t in T] for j in J]


model.objective = xsum(t * x[n + 1][t] for t in T)

for j in J:
    model += xsum(x[j][t] for t in T) == 1

for j in J: 
    model += p[j] + (xsum(t * x[j][t] for t in T)) <= d[j]


for (r, t) in product(R, T):
    model += (
        xsum(u[j][r] * x[j][t2] for j in J for t2 in range(max(0, t - p[j] + 1), t + 1))
        <= c[r])

for (j, s) in S:
    model += xsum(t * x[s][t] - t * x[j][t] for t in T) >= p[j]

model.write('model.lp')

model.optimize()

print("Agendamento: ")
for (j, t) in product(J, T):
    if (x[j][t].x >= 0.99):
        print("Atividade {}: inicio em: t={} finalizando em t={}".format(j, t, t+p[j]))
print("Total = {}".format(model.objective_value))
