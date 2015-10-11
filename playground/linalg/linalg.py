from __future__ import division

import numpy as np


def delim(msg=""):
  print("-"*10,msg,"-"*10)

delim("Playing around")
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


def mtranspose(M):
  cols, rows = len(M[0]),len(M)
  MT = np.zeros( (cols, rows) )
  for ridx, r in enumerate(M):
    for cidx, c in enumerate(r):
      MT[cidx][ridx] = c
  return MT

def symmetric(m):
  mT = np.transpose(m)
  for i in range(0, len(mT)):
    for j in range(0, len(mT)):
      if m[i][j] != mT[i][j]:
        return False
  return True

def LU(a):
  A = np.array(a, copy=True)
  n = len(A)
  tol = 1.e-6

  L = np.zeros( (n, n) )
  for k in range(0, n):
    if abs(A[k][k]) < tol:
      raise Exception("Cannot proceed without row exchanges!")

    L[k][k] = 1
    for i in range(k+1, n):
      L[i][k] = A[i][k]/A[k][k]

      for j in range(k+1,n):
        A[i][j] = A[i][j] - (L[i][k]*A[k][j])

  if not symmetric(A):
    U = np.zeros( (n, n) )
    for k in range(0, n):
      for j in range(k, n):
        U[k][j] = A[k][j]

    return L, U

  return L, np.transpose(L)

def LDU(a):
  n = len(a)
  L, U = LU(a)
  D = np.zeros( (n, n) )
  for k in range(0, n): 
    D[k][k] = U[k][k]
    U[k][k] = 1
  return L, D, U

def solve_for(a, b):
  A = np.array(a, copy=True)
  b = np.array(b, copy=True)
  n = len(A)
  L, U = LU(A)

  s = 0
  c = np.zeros( n )
  for k in range(0, n):
    for j in range(0, k - 1):
      s = s + L[k][j] * c[j]
    c[k] = b[k] - s
    s = 0

  t = 0
  x = np.zeros( n )
  for k in range(n-1,-1,-1):
    for j in range(k+1, n):
      t = t + U[k][j] * x[j]
    x[k] = (c[k] - t)/U[k][k]
  
  return np.transpose(x)

delim("LU decomposition")
A = np.array([[2,1,0],
            [1,2,1],
            [0,1,2]])

L, U = LU(A)
delim("A")
print(A)
delim("L")
print(L)
delim("U")
print(U)
b = [1,2,3]
delim("b")
print(b)
delim("Solve Ab")
print(solve_for(A, b))
delim("LDU decomposition")
L, D, U = LDU(A)
delim("L")
print(L)
delim("D")
print(D)
delim("U")
print(U)

delim("symmetric")
A = [[2,1,0],
     [1,2,1],
     [0,1,2]]
print(symmetric(A))
A = [[1,2],
     [0,1]]
print(symmetric(A))



