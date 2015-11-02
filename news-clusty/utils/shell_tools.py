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
    print("  blaster", 
      colored(cmd, "yellow"), 
      colored("\n\t" + "\n\t".join(descr), "magenta"), "\n")

def pick_date_range(args):
  if not args or len(args) > 2:
    return None, None
  if len(args) == 1:
    return args[0], None
  elif len(args) == 2:
    return args[0], args[1]
