
# Pretty printing formulas
def lowercase_alpha():
  return [chr(i) for i in range(ord('a'), ord('z') + 1)]

def n_sanitized(n):
  if n < 0:
    return n
  return abs(n)

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def normalize_num(n):
  if not is_number(n):
    return n
  var = n_sanitized(n)
  if var < 0:
    var = "(%s)" % var
  return var

def pprint(seq, subst=None):
  if not subst:
    subst = lowercase_alpha()

  var = normalize_num(subst[0])
  offset = ""
  if seq[0] > 0:
    offset = " "

  accu = "%s%s*%s\t" % (offset, seq[0], var)

  matching_character = zip(seq[1:-1], subst[1:])
  for (comp, var) in matching_character:
    var = normalize_num(var)

    if comp < 0:
      comp = abs(comp)
      accu += ("- %s*%s\t" % (comp, var))

    else:
      comp = abs(comp)
      accu += ("+ %s*%s\t" % (comp, var))

  print "%s = %s" % (accu, seq[-1])
