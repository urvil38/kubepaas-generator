import os

def getEnv(name):
  value = os.environ.get(name)
  if value == None:
    return ""
  else:
    return value