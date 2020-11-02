import socket
import sys
import getopt
import Regex
from ServerClass import ServerThread

addr = None
update_period = 4 # Default value for update period

options, remainder = getopt.getopt(sys.argv[1:], 'x', ['addr=',
                                                         'update-period=',
                                                         ])

for opt, arg in options:
    if opt in ('--addr'):
        addr = arg
    elif opt in ('--update-period'):
        update_period = int(arg)

if(addr == None):
    raise ValueError('Valor ADDR nao definidos na linha de comando')
print ('ADDR   :', addr)
print ('UPDATE-PERIOD   :', update_period)



threadServer = ServerThread(addr,55151, update_period)

threadServer.start()




msg = input()

while(msg != '\x18'):
    comandos = msg.split()
    if(Regex.CheckADD(msg)):
        print("Comando ADD Reconhecido")
        threadServer.AddFromTable(comandos[1],comandos[1],comandos[2])
        # print("TABELA ROTEADOR:",threadServer.myRouteTable)
    elif(Regex.CheckDEL(msg)):
        print("Comando DEL Reconhecido")
        threadServer.DelFromTable(comandos[1])
    elif(Regex.CheckTrace(msg)):
        print("Comando Trace Reconhecido")
        threadServer.TraceCommand(comandos[1])
    else:
        print("Comando nao reconhecido")
    # udp.sendto (msg.encode(), dest)
    msg = input()
udp.close()
