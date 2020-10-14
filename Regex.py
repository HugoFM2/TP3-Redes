# Funcoes que detecta os comandos inseridos se estao na formatacao correta
import re


def CheckADD(command):
    return re.search("^add [\d.]+ \d+$", command)

def CheckDEL(command):
    return re.search("^del [\d.]+$", command)






if CheckDEL("del 192.168.15.5"):
  print("YES! We have a match!")
else:
  print("No match")
