import socket
import sys
import getopt
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
    elif opt in ('--host'): # Temporario, remover dps AAA
        HOST = arg
if(HOST == None or addr == None): # Temporario, remover dps o HOST AAA
    raise ValueError('Valor de HOST ou ADDR nao definidos na linha de comando')
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
    udp.sendto (msg.encode(), dest)
    msg = input()
udp.close()
