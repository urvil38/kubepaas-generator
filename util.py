import os

def getEnv(name, default = ""):
  value = os.environ.get(name)
  if value == None:
    return default
  else:
    return value