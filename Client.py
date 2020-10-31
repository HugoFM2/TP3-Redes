import socket
import JSON









def sendData(source,destination,payload):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (destination, 55151)
    msg = JSON.Data(source,destination,payload)
    udp.sendto(msg.encode(),dest)

print('Para sair use CTRL+X\n')
msg = input()

while(msg != '\x18'):
    if msg == "oi":
        sendData("127.0.1.5","127.0.1.1","mensagem aqui")

    udp.sendto (msg.encode(), dest)
    msg = input()
udp.close()
