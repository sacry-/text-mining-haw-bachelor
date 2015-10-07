import numpy as np


A = np.array([[1,1,1,1],[2,2,2,2]])
B = np.array([[2],[3],[4],[5]])

print( np.dot(A, B) )

A = np.array([[1,1],[2,2]])
print( np.dot(A, A) )

E = np.array([[1,0,0],[-2,1,0],[0,0,1]])
A = np.array([[1,2,3],[2,4,6],[1,2,3]])

print( np.dot(E, A) )


idx = 0
for e in A:
  print(e[idx])
  idx += 1