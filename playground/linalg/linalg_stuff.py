import numpy as np
from scipy import linalg

a = np.random.randn(9, 6)

print(a)

U, s, Vh = linalg.svd(a)

print(U)
print(Vh)
print("sigma:",s)
U.shape, Vh.shape, s.shape
