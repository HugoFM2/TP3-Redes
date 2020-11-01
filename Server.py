import socket
import sys
import getopt
import Regex
from ServerClass import ServerThread

BUFSZ = 1024


addr = None
update_period = 4 # Default value for update period
HOST = None # Temporario, remover dps AAA

options, remainder = getopt.getopt(sys.argv[1:], 'x', ['addr=',
                                                         'update-period=',
                                                         'host=', # Temporario, remover dps AAA
                                                         ])

for opt, arg in options:
    if opt in ('--addr'):
        addr = arg
    elif opt in ('--update-period'):
        update_period = arg

if(addr == None):
    raise ValueError('Valor ADDR nao definidos na linha de comando')
print ('ADDR   :', addr)
print ('UPDATE-PERIOD   :', update_period)



threadServer = ServerThread(addr,55151)

threadServer.start()





#Parte do cliente embutido

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, 55151)
print('Para sair use CTRL+X\n')
msg = input()

while(msg != '\x18'):
    comandos = msg.split()
    if(Regex.CheckADD(msg)):
        print("Comando ADD Reconhecido")
        threadServer.AddFromTable(comandos[1],comandos[2])
        print(threadServer.myRouteTable)
    elif(Regex.CheckDEL(msg)):
        print("Comando DEL Reconhecido")
        threadServer.DelFromTable(comandos[1])
    elif(Regex.CheckTrace(msg)):
        print("Comando Trace Reconhecido")
        threadServer.TraceCommand(comandos[1])
    else:
        print("Comando não reconhecido")
    # udp.sendto (msg.encode(), dest)
    msg = input()
udp.close()
