import sys
from termcolor import colored


def consolify():
  cmd, args = None, []
  if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if len(sys.argv) > 2:
      args = [x.lower().strip() for x in sys.argv[2:] if x]
  return cmd, args

def to_shell(description, cmds):
  print("\n", colored(description, "green", attrs=["underline"]))
  for cmd, descr in cmds:
    print("  news-clusty", 
      colored(cmd, "yellow"), 
      colored("\n\t" + "\n\t".join(descr), "magenta"), "\n")

def pick_date_range(args):
  if not args:
    return None, None
  if len(args) == 1:
    return args[0], None
  else:
    return args[0], args[1]

def parse_date_at(args, sidx=0, eidx=2):
  if not args:
    return None, None
  if len(args) <= sidx:
    return args[0], None
  else:
    return args[0], args[1]


