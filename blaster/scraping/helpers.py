import re


DATE_INDEX_PATTERN = re.compile("^(2[0-9]{3})\W+([0-9]{1,2})\W+([0-9]{1,2})")
def date_for_index(date_str):
  m = DATE_INDEX_PATTERN.match(date_str)
  if m:
    return "".join([m.group(x) for x in range(1, 3 + 1)])
  return None