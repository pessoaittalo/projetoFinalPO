from itertools import product
from mip import Model, xsum, BINARY,minimize, INTEGER

n = 14
p = [0,1,2,2,3,2,3,19,2,10,3,5,9,6,9,0]
c = [160,160,160,160,160]
S =  [[0,1],[0,2],[0,3],[1,2],[1,3],[2,4],[2,5],[5,6],[1,7],[1,8],[1,9],[8,10],[5,11],[6,12],[10,13],[9,14],[13,14],[14,15]]
#S = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15]]
w = [0,3,2,2,3,2,5,4,3,2,2,3,4,4,8,0]
d = [0,1,2,2,3,5,19,3,11,6,6,11,17,12,20,144]
u = [[0,0,0,0,0],[4,1,0,5,0],[5,0,0,0,0],[4,1,1,5,10],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0],[4,1,0,5,0]]
(R, J, T) = (range(len(c)), range(len(p)), range(sum(p)+1))
a = []

for j in J:
    aux = []
    for t in T:
        if((p[j] + t) <= d[j]):
            aux.append(0)
        else:
            aux.append((p[j]+t) - d[j])
    a.append(aux)

            
model = Model()
x = [[model.add_var(name="x({},{})".format(j, t), var_type=BINARY) for t in T] for j in J]
model.objective = (xsum(w[j] * a[j][t] * x[j][t] for j in J for t in T))


for j in J:
    model += xsum(x[j][t] for t in T) == 1


for (r, t) in product(R, T):
    model += (
        xsum(u[j][r] * x[j][t2] for j in J for t2 in range(max(0, t - p[j] + 1), t + 1))
        <= c[r])

for (j, s) in S:
    model += xsum(t * x[s][t] - t * x[j][t] for t in T) >= p[j]

model.write('model.lp')


model.optimize()
print("Atraso: ")
for (j, t) in product(J, T):
    if (x[j][t].x >= 0.99):
        print("Atividade {}finalizando em t={}".format(j, t, t+p[j]), " entregou em:", d[j])
print("Total = {}".format(model.objective_value))
