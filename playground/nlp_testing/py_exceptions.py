import time




try:
  1 / 0
except (KeyboardInterrupt, SystemExit):
  raise SystemExit("Keyboard was interrupted - Exiting System")
except Exception as e:
  print(e.__doc__)

try:
  time.sleep(5)
except (KeyboardInterrupt, SystemExit):
  raise SystemExit("\nKeyboard was interrupted - Exiting System")

