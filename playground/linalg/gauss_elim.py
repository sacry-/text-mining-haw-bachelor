from __future__ import division
from print_gauss import pprint, lowercase_alpha, n_sanitized

import numpy as np


# Gauss Algorithm
def indexed(seq):
  return zip(seq, range(0,len(seq)))

def copy_equation(equation):
  return [x for x in equation]

def freduce(elim, subt, pivot_position=0):
  if subt[pivot_position] == 0.0:
    raise Exception("Pivot was Zero! System cannot be eliminated!")

  multiplier = elim[pivot_position] / subt[pivot_position]

  return map(lambda t: t[0] - (subt[t[1]] * multiplier), indexed(elim))

def is_upper_triangular(m):
  mat = np.array( m )
  return np.allclose(mat, np.triu(mat))


def gauss_repair(system, pivot_position):
  count = []
  for rank, equation in enumerate(system):
    c = 0
    for comp in equation:
      if comp != 0.0:
        break
      c += 1
    count.append( (rank, c) )
  
  return map(
    lambda (rank, _): system[rank], 
    sorted(count, key=lambda (_, count): count)
  )

def gauss_elimination(system, head=0, pivot_position=0):
  system = map(lambda x: copy_equation(x), system)
  system = gauss_repair(system, pivot_position)

  ref = system[head]
  base = head + 1

  if base > len(system):
    return system

  new_equations = []
  base_equations = system[base:]
  for idx, equation in enumerate(base_equations):
    new_equation = freduce(equation, ref, pivot_position)
    new_equations.append( (base + idx, new_equation) )

  for (idx, new_equation) in new_equations:
    system[idx] = new_equation

  if not is_upper_triangular(system):
    return gauss_elimination( system, head + 1, pivot_position + 1 )

  return system


def find_unknowns(new_equations):
  # get last equation with first unknown
  last = new_equations[-1]
  first_unknown = last[-1] / last[-2]

  # known memoizes every new found unknown in reversed order
  known = [ first_unknown ]

  # Resolve for the other equations based on the first unknown
  for equation in reversed(new_equations[:-1]):
    r = equation[-1]

    # substitute known variables in persisted in knowns,
    # in current equation
    rev = list(reversed(equation[:-1]))
    for idx in range(0,len(known)):
      rev[idx] = rev[idx] * known[idx]

    # sum everything that could be evaluated thus far
    p1 = sum(rev[:len(known)])

    # basic calculus:
    # x*2 - 20 = r | + 20
    if p1 < 0:
      r += abs(p1)
    # x*2 + 20 = r | - 20
    else:
      r -= p1

    # given 20*a = r
    # get 'a' by a = r / 20
    unkown = r / rev[len(known)]
    known.append( unkown )

  return list(reversed(known))


def transform(f, equations):
  return map(lambda x: 
    map(lambda y: f(y), x), equations
  )

def check_correctness(equation, unknowns):
  s = []
  for idx, comp in enumerate(equation[:-1]):
    s.append( comp * unknowns[idx] )

  correct = sum(s) == equation[-1]

  if not correct:
    print "Expected: %.32f to be: %s! Maybe floating point issues!" % (sum(s), equation[-1])

def print_system(system):
  for equation in system:
    pprint(equation)
  print "-"*20

def solve(system):
  new_system = gauss_elimination(system)
  print_system(new_system)

  unknowns = find_unknowns(new_system)
  alpha = lowercase_alpha()
  for idx, unknown in enumerate(unknowns):
    print "  %s\t=\t%s" % (alpha[idx], n_sanitized(unknown))

  print "-"*20

  for equation in system:
    check_correctness(equation, unknowns)
    pprint(equation, unknowns)


if __name__ == "__main__":
  sys1 = [
    # 2x + 4y - 2z = 2
    [2.0, 4.0, -2.0, 2.0],
    # 4x + 9y - 3z = 8
    [4.0, 9.0, -3.0, 8.0],
    # -2x - 3y + 7z = 10
    [-2.0, -3.0, 7.0, 10.0]
  ]

  sys2 = [ # awkward example, proof of concept...
    [2.0, 4.0, -2.0, 2.0, 2.0],
    [0.0, 0.0, 0.0, 3.0, 8.0],
    [1.0, -3.0, 0.0, 0.0, 10.0],
    [0.0, 3.0, 4.0, 5.0, 10.0]
  ]

  systems = [ sys1, sys2 ]

  for system in systems:
    solve( system )





