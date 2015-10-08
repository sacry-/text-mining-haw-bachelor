import numpy as np


def delim():
  print("-"*40)

A = np.array([[1,1,1,1],[2,2,2,2]])
B = np.array([[2],[3],[4],[5]])
print(A)
print( np.dot(A, B) )

delim()

A = np.array([[1,1],[2,2]])
print( np.dot(A, A) )

delim()

E = np.array([[1,0,0],[-2,1,0],[0,0,1]])
A = np.array([[1,2,3],[2,4,6],[1,2,3]])

print( np.dot(E, A) )

delim()

def transpose(M):
  cols, rows = len(M[0]),len(M)
  MT = np.zeros( (cols, rows) )
  for ridx, r in enumerate(M):
    for cidx, c in enumerate(r):
      MT[cidx][ridx] = c
  return MT

A = np.array([[1,2,3],[0,0,4]])
B = np.array([[1,2,3],[0,0,4],[1,2,3]])
print( A )
print( transpose(A) )


