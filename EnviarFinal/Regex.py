# Funcoes que detecta os comandos inseridos se estao na formatacao correta
import re

def CheckADD(command):
    return re.search("^add [\d.]+ \d+$", command)

def CheckDEL(command):
    return re.search("^del [\d.]+$", command)

def CheckTrace(command):
    return re.search("^trace [\d.]+$", command)
